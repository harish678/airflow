from airflow import DAG
from datetime import datetime
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    "start_date": datetime(2020, 12, 1),
    "owner": "airflow",
    "retries": 0
}

with DAG(dag_id="dynamic_dag",
         schedule_interval="@daily",
         default_args=default_args,
         catchup=False) as dag:

    opr_end = BashOperator(task_id="opr_end", bash_command="echo 'DONE'")

    # Dynamic Definition of DAG
    for counter in range(1, 4):
        task_id = 'opr_insert_' + str(counter)
        task_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        opr_insert = PostgresOperator(
            task_id=task_id,
            sql="insert into airflow_mdb (id, timestamp) values ('" + task_id + "-" + \
                    task_date + "', '" + task_date + "');",
            postgres_conn_id="postgres",
            autocommit=True,
            database="scenarios")

        opr_insert >> opr_end
