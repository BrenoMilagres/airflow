export AIRFLOW_HOME="$(pwd)/airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW_CONN_CAPIM_POSTGRES_DB="postgres://capim:capim@localhost:5432/capim"

mkdir airflow
cp -R dags airflow

# initialize the database
airflow users  create --role Admin --username capim --email admin --firstname admin --lastname admin --password capim
airflow standalone

