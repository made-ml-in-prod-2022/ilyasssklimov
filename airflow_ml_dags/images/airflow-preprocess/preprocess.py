import click
import pandas
from sklearn.preprocessing import StandardScaler
import os


def transform_data(data: pandas.DataFrame) -> pandas.DataFrame:
    scaler = StandardScaler()
    transformed_data = scaler.fit_transform(data)


@click.command('preprocess_data')
@click.option('--input-dir', help='Input directory from which data is read')
@click.option('--output-dir', help='Output directory to transformed data')
def preprocess_data(input_dir: str, output_dir: str) -> None:
    data = pandas.read_csv(os.path.join(input_dir, 'data.csv'))
    target = pandas.read_csv(os.path.join(input_dir, 'target.csv'))

    os.makedirs(output_dir, exist_ok=True)
    data.to_csv(os.path.join(output_dir, 'data.csv'))
    target.to_csv(os.path.join(output_dir, 'target.csv'))


if __name__ == '__main__':
    preprocess_data()
