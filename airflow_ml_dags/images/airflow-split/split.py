import click
import pandas
from sklearn.model_selection import train_test_split
import os
from typing import Tuple, List

STATE = 123


def save_split_data(datasets: Tuple[pandas.DataFrame], names: List[str], output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    for dataset, name in zip(datasets, names):
        dataset.to_csv(os.path.join(output_dir, f'{name}.csv'), index=False)


@click.command('split_data')
@click.option('--input-dir', help='Input directory from which preprocessed data is read')
@click.option('--output-dir', help='Output directory to split data')
@click.option('--test-size', help='Test size to split dataset', default=0.3, type=float)
def split_data(input_dir: str, output_dir: str, test_size: float) -> None:
    data = pandas.read_csv(os.path.join(input_dir, 'data.csv'))
    target = pandas.read_csv(os.path.join(input_dir, 'target.csv'))
    datasets = train_test_split(data, target, test_size=test_size, random_state=STATE)

    names = ['x_train', 'x_test', 'y_train', 'y_test']
    save_split_data(datasets, names, output_dir)


if __name__ == '__main__':
    split_data()
