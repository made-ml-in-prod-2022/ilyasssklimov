import click
import pandas
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import os
import pickle

STATE = 123


def get_metrics(model: LogisticRegression, x_test: pandas.DataFrame, y_test: pandas.DataFrame) -> str:
    y_pred = model.predict(x_test)
    metrics = classification_report(y_test, y_pred)
    return metrics


def save_metrics(metrics: str, output_dir: str) -> None:
    with open(os.path.join(output_dir, 'metrics_log_reg.txt'), 'w') as f:
        f.write(metrics)


@click.command('validate_model')
@click.option('--input-model-dir', help='Input directory from which model is read')
@click.option('--input-test-dir', help='Input directory from which test data is read')
def validate_model(input_model_dir: str, input_test_dir: str) -> None:
    with open(os.path.join(input_model_dir, 'log_reg.pkl'), 'rb') as f:
        model = pickle.load(f)

    x_test = pandas.read_csv(os.path.join(input_test_dir, 'x_test.csv'))
    y_test = pandas.read_csv(os.path.join(input_test_dir, 'y_test.csv'))

    metrics = get_metrics(model, x_test, y_test)
    save_metrics(metrics, input_model_dir)


if __name__ == '__main__':
    validate_model()
