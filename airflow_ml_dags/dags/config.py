from airflow.models import Variable
from datetime import timedelta


DATA_FOLDER = '/data/raw/{{ ds }}'

PROCESS_FOLDER = '/data/processed/{{ ds }}'
TEST_PROCESS_FOLDER = '/data/test_processed/{{ ds }}'

MODEL_FOLDER = '/data/models/{{ ds }}'
PREDICTION_FOLDER = '/data/predictions/{{ ds }}'

RELATIVE_DATA_FOLDER = 'data/raw/{{ ds }}'
USED_MODEL = Variable.get('MODEL_PATH')
HOST_FOLDER = Variable.get('HOST_FOLDER')

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
