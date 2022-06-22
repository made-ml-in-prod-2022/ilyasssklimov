import click
import pandas
from sklearn.model_selection import train_test_split
import os

STATE = 123


@click.command('split_data')
@click.option('--input-dir', help='Input directory from which preprocessed data is read')
@click.option('--output-dir', help='Output directory to split data')
@click.option('--test-size', help='Test size to split dataset', default=0.3, type=float)
def split_data(input_dir: str, output_dir: str, test_size: float) -> None:
    data = pandas.read_csv(os.path.join(input_dir, 'data.csv'))
    target = pandas.read_csv(os.path.join(input_dir, 'target.csv'))
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=test_size, random_state=STATE)

    os.makedirs(output_dir, exist_ok=True)
    x_train.to_csv(os.path.join(output_dir, 'x_train.csv'), index=False)
    x_test.to_csv(os.path.join(output_dir, 'x_test.csv'), index=False)
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)


if __name__ == '__main__':
    split_data()
