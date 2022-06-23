from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount
import os
from pendulum import today
import config as cfg

TEST_SIZE = 0.3


with DAG(
        'model_train',
        default_args=cfg.default_args,
        schedule_interval='@daily',
        start_date=today('UTC').add(days=-7)
) as dag:
    start = EmptyOperator(task_id='start_model_train')

    data_wait = FileSensor(
        filepath=os.path.join(cfg.FULL_DATA_FOLDER, 'data.csv'),
        poke_interval=60,
        timeout=600,
        mode='poke',
        task_id='wait_for_data'
    )
    target_wait = FileSensor(
        filepath=os.path.join(cfg.FULL_DATA_FOLDER, 'target.csv'),
        poke_interval=60,
        timeout=600,
        mode='poke',
        task_id='wait_for_target')

    preprocess = DockerOperator(
        image='airflow-preprocess',
        command=f'--input-dir={cfg.DATA_FOLDER} --output-dir={cfg.PREPROCESS_FOLDER}',
        task_id='data_preprocess',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')]
    )

    split = DockerOperator(
        image='airflow-split',
        command=f'--input-dir={cfg.PREPROCESS_FOLDER} --output-dir={cfg.SPLIT_FOLDER} --test-size={TEST_SIZE}',
        task_id='data_split',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')]
    )

    train = DockerOperator(
        image='airflow-train',
        command=f'--input-dir={cfg.SPLIT_FOLDER} --output-dir={cfg.MODEL_FOLDER}',
        task_id='model_train',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')]
    )

    validate = DockerOperator(
        image='airflow-validate',
        command=f'--input-model-dir={cfg.MODEL_FOLDER} --input-test-dir={cfg.SPLIT_FOLDER}',
        task_id='model_validate',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')]
    )

    end = EmptyOperator(task_id='end_model_train')

    start >> [data_wait, target_wait] >> preprocess >> split >> train >> validate >> end
