from airflow.models import Variable
from datetime import timedelta


DATA_FOLDER = '/data/raw/{{ ds }}'
PREPROCESS_FOLDER = '/data/processed/{{ ds }}'
SPLIT_FOLDER = '/data/split/{{ ds }}'
HOST_FOLDER = Variable.get('HOST_FOLDER')
FULL_DATA_FOLDER = '/opt/airflow' + DATA_FOLDER

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
