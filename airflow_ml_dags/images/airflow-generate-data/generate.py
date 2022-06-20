import click
import pandas
from sklearn.datasets import load_breast_cancer
import typing
import os

N_SAMPLES = 100
DEFAULT_STATE = 123


def get_data(state: int) -> typing.Tuple[pandas.DataFrame, pandas.Series]:
    data_frame = load_breast_cancer(as_frame=True).frame
    data = data_frame.sample(n=N_SAMPLES, random_state=state)
    return data.loc[:, data.columns != 'target'], data['target']


@click.command('generate_data')
@click.option('--output-dir', help='Output directory to data and target')
def generate_data(output_dir: str) -> None:
    try:
        state = int(output_dir.split('-')[-1])
    except ValueError:
        state = DEFAULT_STATE

    data, target = get_data(state)
    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(os.path.join(output_dir, 'data.csv'), index=False)
    target.to_csv(os.path.join(output_dir, 'target.csv'), index=False)
