# Importing necessary modules
# from datetime import datetime, timedelta
# from airflow import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
# import requests
from os.path import realpath
from json import load
import psycopg2
import datetime
import pendulum
# import os
from airflow.decorators import dag, task



def get_data_from_file():
    base_dir = "/".join(realpath(__file__).split("/")[:-1])
    path = f"{base_dir}/json_for_case.json"

    with open(path) as f:
        data = load(f)
        return data


def transform_the_data():
    transformed_data = []
    book_data = get_data_from_file()
    for book in book_data:
        nome = book['nome']
        idade = book['idade']
        email = book['email']
        telefone = book['telefone']
        logradouro = book['endereco']['logradouro']
        numero = book['endereco']['numero']
        bairro = book['endereco']['bairro']
        cidade = book['endereco']['cidade']
        estado = book['endereco']['estado']
        cep = book['endereco']['cep']

        transformed_data.append((
            nome,
            idade,
            email,
            telefone,
            logradouro,
            numero,
            bairro,
            cidade,
            estado,
            cep
        ))

    return transformed_data


@dag(
    dag_id="json_inputs",
    schedule_interval="@daily",
    start_date=pendulum.datetime(2024, 4, 25, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)
def input_data():
    @task
    def insert_records():
        pg_hook = PostgresHook(postgres_conn_id='capim_postgres_db')
        connection = pg_hook.get_conn()
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS capim_json_inputs (
                id SERIAL PRIMARY KEY,
                nome VARCHAR,
                idade INT,
                email VARCHAR,
                telefone VARCHAR,
                logradouro VARCHAR,
                numero INT,
                bairro VARCHAR,
                cidade VARCHAR,
                estado VARCHAR,
                cep VARCHAR
            )
            """
        )

        transformed_data = transform_the_data()
        for record in transformed_data:
            cursor.execute(
                """
                INSERT INTO capim_json_inputs (
                    nome,
                    idade,
                    email,
                    telefone,
                    logradouro,
                    numero,
                    bairro,
                    cidade,
                    estado,
                    cep
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                record
            )

        cursor.execute(
            """
            DELETE  FROM
                capim_json_inputs a
                    USING capim_json_inputs b
            WHERE
                a.id < b.id
                AND a.nome = b.nome
                AND a.email = b.email
                AND a.idade = b.idade;
            """
        )

        connection.commit()
        cursor.close()
        connection.close()

    insert_records()


dag = input_data()
