from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount
import os
from pendulum import today
import config as cfg
from airflow.utils.email import send_email

TEST_SIZE = 0.3


with DAG(
        'model_train',
        default_args=cfg.default_args,
        schedule_interval='@daily',
        start_date=today('UTC').add(days=-7)
) as dag:
    start = EmptyOperator(task_id='start_model_train')

    data_wait = FileSensor(
        filepath=os.path.join(cfg.RELATIVE_DATA_FOLDER, 'data.csv'),
        poke_interval=30,
        timeout=600,
        mode='poke',
        task_id='wait_for_data',
        email_on_failure=True,
        # on_failure_callback=cfg.log_failure
    )

    target_wait = FileSensor(
        filepath=os.path.join(cfg.RELATIVE_DATA_FOLDER, 'target.csv'),
        poke_interval=30,
        timeout=600,
        mode='poke',
        task_id='wait_for_target',
        on_failure_callback=cfg.log_failure
    )

    preprocess = DockerOperator(
        image='airflow-preprocess',
        command=f'--input-dir={cfg.DATA_FOLDER} --output-dir={cfg.PROCESS_FOLDER} --train',
        task_id='data_preprocess',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        on_failure_callback=cfg.log_failure
    )

    split = DockerOperator(
        image='airflow-split',
        command=f'--input-dir={cfg.PROCESS_FOLDER} --output-dir={cfg.PROCESS_FOLDER} --test-size={TEST_SIZE}',
        task_id='data_split',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        on_failure_callback=cfg.log_failure
    )

    train = DockerOperator(
        image='airflow-train',
        command=f'--input-dir={cfg.PROCESS_FOLDER} --output-dir={cfg.MODEL_FOLDER}',
        task_id='model_train',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        on_failure_callback=cfg.log_failure
    )

    validate = DockerOperator(
        image='airflow-validate',
        command=f'--input-model-dir={cfg.MODEL_FOLDER} --input-test-dir={cfg.PROCESS_FOLDER}',
        task_id='model_validate',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        on_failure_callback=cfg.log_failure
    )

    end = EmptyOperator(task_id='end_model_train')

    start >> [data_wait, target_wait] >> preprocess >> split >> train >> validate >> end
