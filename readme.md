# Capim code

Nesse repositório encontra-se todo o ferramental necessário para executar um ambiente de airflow localmente e subir um banco postgres, além disso foi implementada uma DAG que fará a ingestão de um arquivo json para o banco postgres.

Para orquestrar esse pipeline escolhi o airflow pois é uma ferramenta open source e super tranquila de se implementar, além de oferecer várias features que facilitam o fluxo de trabalho para um engenheiro de dados. 

- Orquestração de Tarefas
- Agendamento 
- Monitoramento e Gerenciamento
- Flexibilidade 
- Reutilização e Modularidade

Seria possível entregar um ambiente baseado em airflow em provedoras de cloud como por exemplo AWS ou GCP. É possível utilizar uma arquitera baseada em containers (self-hosted) ou até mesmo um airflow totalemte gerenciado como por exemplo:

- Cloud Composer GCP (https://cloud.google.com/composer?hl=pt-BR)
- Amazon Managed Workflows (https://aws.amazon.com/pt/managed-workflows-for-apache-airflow/)

Nota: escolher os serviços totalmente gerenciados costuma ser mais caro, porém a sustentação e implementação se tornam bem mais fáceis. 

## Setup (linux ou wsl)

instale o virtualenv
```
python -m pip install --user virtualenv
```

crie um ambiente virtual e o ative
```
virtualenv venv -p python3 && source venv/bin/activate
```

instale as dependencias
```
pip install -r requirements.txt
```

Execute o banco postgres 
(necessário docker e compose instalados na máquina https://docs.docker.com/engine/install/)
```
docker compose up -d
```

Execute o airflow através do airflow_up.sh
```
source airflow_up.sh
```

A partir desse passo você já será capaz de interagir com o WebAPP do airflow no seu navegador

- endereço: localhost:8080
- user: capim
- senha: capim

## Executando a DAG 

Com o WebApp aberto vá até a lista de DAGs e execute a DAG: json_inputs, ela fará a ingestão do arquivo json para uma tabela chamada: capim_json_inputs. Pode-se validar o conteúdo da tabela com o dbeaver (https://dbeaver.io/download/)

Foi adotado que o id não será ingerido dos arquivos json mas sim auto-incrementado pelo banco como um chave primária (PK)

Dessa forma a estratégia de deduplicação consiste em comparar três campos: nome, idade e email. Caso esses 3 campos sejam iguais persistiremos na tabela apenas o campo cujo id é maior (útlima ocorrência)

Pode-se confirmar esse comportamento rodando a DAG mais de uma vez, ela fará a ingestão dos registros, se nenhuma alteração for feita no json todos os registros seriam duplicados na segunda execução, porém com essa estretégia pode-se notar que apenas os registros com maior ID serão mantidos na tabela. 
