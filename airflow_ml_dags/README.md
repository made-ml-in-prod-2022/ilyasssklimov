## Переменные окружения
~~~
export FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")
export HOST_FOLDER="/path/to/host/folder/"
export MODEL_PATH="/path/to/model/model.pkl"
~~~

### Пример (для Windows)
~~~
$env:FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")
$env:HOST_FOLDER="D:/IT/Python/vk_ProdML/ilyasssklimov/airflow_ml_dags/data/"
$env:MODEL_PATH="data/models/2022-06-21/log_reg.pkl"
~~~

## Запуск
~~~
git clone https://github.com/made-ml-in-prod-2022/ilyasssklimov.git
cd ilyasssklimov
git checkout homework3
cd airflow_ml_dags
docker compose up --build
~~~

