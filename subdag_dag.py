import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from airflow import DAG
from datetime import datetime
from airflow.executors.local_executor import LocalExecutor
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from data_pipelines.subdag_factory import subdag_factory

PARENT_DAG_NAME = "subdag_dag"
SUBDAG_DAG_NAME = "subdag"

with DAG(dag_id=PARENT_DAG_NAME,
         schedule_interval="@daily",
         start_date=datetime(2020, 12, 1, 10, 00, 00),
         catchup=False) as dag:

    start_task = DummyOperator(task_id="start")
    subdag_task = SubDagOperator(task_id=SUBDAG_DAG_NAME,
                                 executor=LocalExecutor(),
                                 subdag=subdag_factory(PARENT_DAG_NAME,
                                                       SUBDAG_DAG_NAME,
                                                       dag.start_date,
                                                       dag.schedule_interval))
    end_task = DummyOperator(task_id="end")

    start_task >> subdag_task >> end_task
