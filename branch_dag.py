from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresHook
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

default_args = {
    "start_date": datetime(2020, 12, 1),
    "owner": "airflow",
    "depend_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}


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


def source_to_use(**kwargs):
    # task instance object provided by airflow
    ti = kwargs["ti"]
    date = ti.xcom_pull(task_ids="hook_task")
    print(f"Date of instance_1 fetched from XCOM: {date}")
    return date


def check_for_instance_1(**kwargs):
    ti = kwargs['ti']
    # must return the 'task_id' for the next execution
    # task_id = ti.xcom_pull(task_ids="xcom_task").lower()
    # return task_id
    return 's3'


with DAG(dag_id="branch_dag",
         schedule_interval="@once",
         default_args=default_args,
         catchup=False) as dag:

    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id="hook_task",
                               python_callable=get_activated_sources)
    xcom_task = PythonOperator(task_id="xcom_task",
                               python_callable=source_to_use,
                               provide_context=True)
    branch_task = BranchPythonOperator(task_id="branch_task",
                                       python_callable=check_for_instance_1,
                                       provide_context=True)
    mysql_task = BashOperator(task_id="mysql", bash_command="echo !! mysql !!")
    postgres_task = BashOperator(task_id="postgres",
                                 bash_command="echo !! postgres !!")
    s3_task = BashOperator(task_id="s3", bash_command="echo !! s3 !!")
    mongo_task = BashOperator(task_id="mongo", bash_command="echo !! mongo !!")

    start_task >> hook_task >> xcom_task >> branch_task
    branch_task >> mysql_task
    branch_task >> s3_task
    branch_task >> postgres_task
    branch_task >> mongo_task