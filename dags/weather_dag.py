from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/app')
from main import main  # Assurez-vous que main.py a une fonction main() exécutable

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_data_dag',
    default_args=default_args,
    description='DAG to fetch weather data',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2025, 5, 9),
    catchup=False,
) as dag:

    fetch_weather_data = PythonOperator(
        task_id='fetch_weather_data',
        python_callable=main,
    )

    fetch_weather_data