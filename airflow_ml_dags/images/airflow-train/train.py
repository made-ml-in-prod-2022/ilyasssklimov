import click
import pandas
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
import os
import pickle

STATE = 123


def save_model(model: BaseEstimator, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'log_reg.pkl'), 'wb') as f:
        pickle.dump(model, f)


@click.command('train_model')
@click.option('--input-dir', help='Input directory from which data is read')
@click.option('--output-dir', help='Output directory to save model')
def train_model(input_dir: str, output_dir: str) -> None:
    x_train = pandas.read_csv(os.path.join(input_dir, 'x_train.csv'))
    y_train = pandas.read_csv(os.path.join(input_dir, 'y_train.csv'))

    log_reg = LogisticRegression(random_state=STATE)
    log_reg.fit(x_train, y_train)
    save_model(log_reg, output_dir)


if __name__ == '__main__':
    train_model()
