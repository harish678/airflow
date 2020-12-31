import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from airflow import DAG
from datetime import datetime
from data_pipelines import fetching_tweet, cleaning_tweet
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator

default_args = {"start_date": datetime(2020, 1, 1), "owner": "airflow"}

# catchup=False, will trigger only the most recent DAG run instead of all pending from the start_date
with DAG(dag_id="twitter_dag",
         schedule_interval="@daily",
         default_args=default_args,
         catchup=False) as dag:
    # check for file existance every 5 seconds
    waiting_for_tweets = FileSensor(task_id="waiting_for_tweets",
                                    fs_conn_id="fs_tweet",
                                    filepath="data.csv",
                                    poke_interval=5)

    fetching_tweets = PythonOperator(task_id="fetching_tweets",
                                     python_callable=fetching_tweet.main)

    cleaning_tweets = PythonOperator(task_id="cleaning_tweets",
                                     python_callable=cleaning_tweet.main)

    waiting_for_tweets >> fetching_tweets >> cleaning_tweets
