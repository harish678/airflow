from airflow import DAG
from datetime import datetime
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2020, 12, 1),
    'dependent_on_past': False
}


def create_variable():
    _ = Variable.set("my_var", "Harish Vutukuri")


def display_variable():
    my_var = Variable.get("my_var")
    print(f"Variable: {my_var}")


with DAG(dag_id="variable_dag",
         schedule_interval="@once",
         default_args=default_args,
         catchup=False) as dag:

    create_task = PythonOperator(task_id="create_variable",
                                 python_callable=create_variable)
    display_task = PythonOperator(task_id="display_variable",
                                  python_callable=display_variable)

    create_task >> display_task
