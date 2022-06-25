from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from airflow.sensors.filesystem import FileSensor
from docker.types import Mount
import os
from pendulum import today
import config as cfg


with DAG(
        'target_predict',
        default_args=cfg.default_args,
        schedule_interval='@daily',
        start_date=today('UTC').add(days=-7)
) as dag:
    start = EmptyOperator(task_id='start_target_predict')

    data_wait = FileSensor(
        filepath=os.path.join(cfg.RELATIVE_DATA_FOLDER, 'data.csv'),
        poke_interval=30,
        timeout=600,
        mode='poke',
        task_id='wait_for_data',
        email_on_failure=True
    )

    model_wait = FileSensor(
        filepath=cfg.USED_MODEL,
        poke_interval=30,
        timeout=600,
        mode='poke',
        task_id='wait_for_model',
        email_on_failure=True
    )

    preprocess = DockerOperator(
        image='airflow-preprocess',
        command=f'--input-dir={cfg.DATA_FOLDER} --output-dir={cfg.TEST_PROCESS_FOLDER} --test',
        task_id='data_preprocess',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        email_on_failure=True
    )

    predict = DockerOperator(
        image='airflow-predict',
        command=f'--model={cfg.USED_MODEL} --input-dir={cfg.TEST_PROCESS_FOLDER} --output-dir={cfg.PREDICTION_FOLDER}',
        task_id='target_predict',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        email_on_failure=True
    )

    end = EmptyOperator(task_id='end_target_predict', on_success_callback=cfg.log_success)

    start >> [data_wait, model_wait] >> preprocess >> predict >> end
