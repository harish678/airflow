from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator


def log_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(
        f"SLA was missed on DAG {dag.dag_id}s by task is {slas}s with task list: \
            {task_list} which are blocking task id {blocking_tis}s with task list: {blocking_task_list}"
    )


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 1, 1, 23, 15, 0),
    "depend_on_past": False,
    "email": None,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}

with DAG(dag_id="sla_dag",
         schedule_interval="*/1 * * * *",
         default_args=default_args,
         sla_miss_callback=log_sla_miss,
         catchup=False) as dag:

    t0 = DummyOperator(task_id="t0")

    t1 = BashOperator(task_id="t1",
                      bash_command="sleep 15",
                      sla=timedelta(seconds=5),
                      retries=0)

    t0 >> t1
