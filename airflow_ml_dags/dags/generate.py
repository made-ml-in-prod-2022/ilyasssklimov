from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.empty import EmptyOperator
from datetime import timedelta
from docker.types import Mount
from pendulum import today


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


with DAG(
        'data_acquisition',
        default_args=default_args,
        schedule_interval='@daily',
        start_date=today('UTC').add(days=-7)
) as dag:
    start = EmptyOperator(task_id='start_data_acquisition')

    generate = DockerOperator(
        image='airflow-generate-data',
        task_id="generate_data",
        command='--output-dir=/data/raw/{{ ds }}',
        network_mode="bridge",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=[
            Mount(
                source='D:/IT/Python/vk_ProdML/ilyasssklimov/airflow_ml_dags/data/',
                target='/data',
                type='bind'
            )
        ]
    )

    end = EmptyOperator(task_id='end_data_acquisition')

    start >> generate >> end
