from airflow.utils.context import Context
from airflow.utils.email import send_email_smtp
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


def log_success(context):
    dag_run = context.get('dag_run')
    logging.info(f'DAG {dag_run} is successfully completed')
    msg = "DAG ran successfully"
    subject = f"DAG {dag_run} has completed"
    send_email_smtp(to='ilyasssklimov@gmail.com', subject=subject, html_content=msg)


def log_failure(context: Context):
    dag_run = context.get('dag_run')
    task_instances = dag_run.get_task_instances()
    logging.error(f'DAG {dag_run} is failed, not success tasks instances: {task_instances}')


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'on_success_callback': log_success,
    'email': ['ilyasssklimov@gmail.com'],
    'email_on_failure': True
}
