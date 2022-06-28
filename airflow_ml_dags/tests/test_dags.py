import pytest
from airflow.models import DagBag, Variable
import sys


DAGS_PATH = '../dags/'
sys.path.append(DAGS_PATH)
Variable.set(key='MODEL_PATH', value=None)
Variable.set(key='HOST_FOLDER', value=None)


@pytest.fixture()
def dagbag():
    return DagBag(dag_folder=DAGS_PATH, include_examples=False)


def test_base_generate_dag(dagbag):
    dag = dagbag.get_dag(dag_id='data_generate')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 3


def test_base_train_dag(dagbag):
    dag = dagbag.get_dag(dag_id='model_train')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 8


def test_base_predict_dag(dagbag):
    dag = dagbag.get_dag(dag_id='target_predict')
    assert dagbag.import_errors == {}
    assert dag is not None
    assert len(dag.tasks) == 6


def assert_dag_dict_equal(source, dag):
    assert dag.task_dict.keys() == source.keys()
    for task_id, downstream_list in source.items():
        assert dag.has_task(task_id)
        task = dag.get_task(task_id)
        assert task.downstream_task_ids == set(downstream_list)


def test_tasks_generate_dag(dagbag):
    dag = dagbag.get_dag(dag_id='data_generate')
    tasks = {
        'start_data_generate': ['data_generate'],
        'data_generate': ['end_data_generate'],
        'end_data_generate': []
    }
    assert_dag_dict_equal(tasks, dag)


def test_tasks_train_dag(dagbag):
    dag = dagbag.get_dag(dag_id='model_train')
    tasks = {
        'start_model_train': ['wait_for_data', 'wait_for_target'],
        'wait_for_data': ['data_preprocess'],
        'wait_for_target': ['data_preprocess'],
        'data_preprocess': ['data_split'],
        'data_split': ['model_train'],
        'model_train': ['model_validate'],
        'model_validate': ['end_model_train'],
        'end_model_train': []
    }
    assert_dag_dict_equal(tasks, dag)


def test_tasks_predict_dag(dagbag):
    dag = dagbag.get_dag(dag_id='target_predict')
    tasks = {
        'start_target_predict': ['wait_for_data', 'wait_for_model'],
        'wait_for_data': ['data_preprocess'],
        'wait_for_model': ['data_preprocess'],
        'data_preprocess': ['target_predict'],
        'target_predict': ['end_target_predict'],
        'end_target_predict': []
    }
    assert_dag_dict_equal(tasks, dag)
