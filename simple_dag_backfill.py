from airflow import DAG
from datetime import datetime
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    "start_date": datetime(2020, 12, 1),
    "owner": "airflow",
    "concurrency": 1,
    "retries": 0
}

with DAG(dag_id="simple_dag_backfill",
         schedule_interval="@daily",
         default_args=default_args) as dag:

    task_hello = BashOperator(task_id="hello", bash_command="echo 'hello!'")
    task_bye = BashOperator(task_id="bye", bash_command="echo bye")

    task_hello >> task_bye
