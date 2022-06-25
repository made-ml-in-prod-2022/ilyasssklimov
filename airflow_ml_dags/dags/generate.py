from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from docker.types import Mount
from pendulum import today
import config as cfg


with DAG(
        'data_generate',
        default_args=cfg.default_args,
        schedule_interval='@daily',
        start_date=today('UTC').add(days=-7)
) as dag:
    start = EmptyOperator(task_id='start_data_generate')

    generate = DockerOperator(
        image='airflow-generate',
        task_id='data_generate',
        command=f'--output-dir={cfg.DATA_FOLDER}',
        network_mode='bridge',
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[Mount(source=cfg.HOST_FOLDER, target='/data', type='bind')],
        on_failure_callback=cfg.log_failure
    )

    end = EmptyOperator(task_id='end_data_generate')

    start >> generate >> end
