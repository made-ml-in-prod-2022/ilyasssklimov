from fastapi import FastAPI
import logging
import numpy as np
import os
import pandas as pd
import pickle
from pydantic import BaseModel
from sklearn.pipeline import Pipeline
from typing import List, Optional
import uvicorn


app = FastAPI()
logger = logging.getLogger(__name__)
model: Optional[Pipeline] = None


class BreastCancerModel(BaseModel):
    data: List[List[float]]
    features: List[str]


class CancerResponse(BaseModel):
    cancer: int


def read_model(path: str) -> Pipeline:
    with open(path, 'rb') as f:
        return pickle.load(f)


def make_predict(data: List, features: List[str], model_: Pipeline) -> List[CancerResponse]:
    data = pd.DataFrame(data, columns=features)
    predicts = np.exp(model_.predict(data))
    return [CancerResponse(cancer=int(cancer)) for cancer in predicts]


@app.get('/')
def main():
    return 'It is entry point of our predictor'


@app.on_event('startup')
def load_model():
    global model
    model_path = os.getenv('PATH_TO_MODEL')
    if model_path is None:
        err = f'PATH_TO_MODEL {model_path} is None'
        logger.error(err)
        raise RuntimeError(err)

    model = read_model(model_path)


@app.get('/healz')
def health() -> bool:
    return not (model is None)


@app.get('/predict', response_model=List[CancerResponse])
def predict(request: BreastCancerModel):
    return make_predict(request.data, request.features, model)


if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', port=8000)
