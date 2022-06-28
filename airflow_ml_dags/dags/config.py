from airflow.utils.context import Context
from airflow.models import Variable
from datetime import timedelta
import logging


DATA_FOLDER = '/data/raw/{{ ds }}'

PROCESS_FOLDER = '/data/processed/{{ ds }}'
TEST_PROCESS_FOLDER = '/data/test_processed/{{ ds }}'

MODEL_FOLDER = '/data/models/{{ ds }}'
PREDICTION_FOLDER = '/data/predictions/{{ ds }}'

RELATIVE_DATA_FOLDER = 'data/raw/{{ ds }}'
USED_MODEL = Variable.get('MODEL_PATH')
HOST_FOLDER = Variable.get('HOST_FOLDER')


def log_success(context: Context) -> None:
    dag_run = context.get('dag_run')
    message = f'DAG is successfully completed:\n{dag_run}'
    logging.info(f'{message}\nAirflow Webserver URL: http://localhost:8080')


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email': ['ilyasssklimov@gmail.com'],
    'email_on_failure': False
}
