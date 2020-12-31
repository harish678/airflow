from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresHook

default_args = {
    "start_date": datetime(2020, 12, 1),
    "owner": "airflow",
    "depend_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}


def get_activated_sources():
    query = "select * from airflow_mdb"
    # connection used in airflow UI
    postgres_hook = PostgresHook(postgres_conn_id="postgres",
                                 schema="scenarios")
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    for res in results:
        print(f"ID: {res[0]}, TIMESTAMP: {res[1]}")


with DAG(dag_id="hook_dag",
         schedule_interval="@once",
         default_args=default_args,
         catchup=False) as dag:

    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id="hook_task",
                               python_callable=get_activated_sources)

    start_task >> hook_task
