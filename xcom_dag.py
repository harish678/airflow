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


# No need to call "xcom_push" as we are using "return" (which has same effect)
def get_activated_sources():
    query = "select * from airflow_mdb"
    postgres_hook = PostgresHook(postgres_conn_id="postgres",
                                 schema="scenarios")
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    for res in results:
        if "insert_1" in res[0]:
            return res[1]
    return None


"""
# same above method with "xcom_push"
def get_activated_sources(**kwargs):
    ti = kwargs['ti']
    query = "select * from airflow_mdb"
    postgres_hook = PostgresHook(postgres_conn_id="postgres",
                                 schema="scenarios")
    connection = postgres_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    for res in results:
        if res[1]:
            ti.xcom_push(key="activated_source", value=res[0])
            return None
    return None
"""


def source_to_use(**kwargs):
    # task instance object provided by airflow
    ti = kwargs["ti"]
    date = ti.xcom_pull(task_ids="hook_task")
    print(f"Date of instance_1 fetched from XCOM: {date}")


with DAG(dag_id="xcom_dag",
         schedule_interval="@once",
         default_args=default_args,
         catchup=False) as dag:

    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id="hook_task",
                               python_callable=get_activated_sources)
    xcom_task = PythonOperator(task_id="xcom_task",
                               python_callable=source_to_use,
                               provide_context=True)
    start_task >> hook_task >> xcom_task