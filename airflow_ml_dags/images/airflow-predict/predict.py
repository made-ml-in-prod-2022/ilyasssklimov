import click
import pandas
import os
import pickle

STATE = 123


@click.command('predict_target')
@click.option('--model', help='Used model to predict')
@click.option('--input-dir', help='Input directory from which preprocessed test data is read')
@click.option('--output-dir', help='Output directory to save predictions')
def predict_target(model: str, input_dir: str, output_dir: str) -> None:
    with open(model, 'rb') as f:
        model = pickle.load(f)
    data = pandas.read_csv(os.path.join(input_dir, 'data.csv'))
    y_pred = pandas.Series(model.predict(data), name='target')

    os.makedirs(output_dir, exist_ok=True)
    y_pred.to_csv(os.path.join(output_dir, 'predictions.csv'), index=False)


if __name__ == '__main__':
    predict_target()
