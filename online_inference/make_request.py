import pandas as pd
import requests


if __name__ == '__main__':
    data = pd.read_csv('./data/data.csv')
    request_features = list(data.columns)

    for i in range(100):
        request_data = [float(x) for x in data.iloc[i].tolist()]
        print(request_data)
        response = requests.get(
            'http://localhost:8000/predict',
            json={
                'data': [request_data],
                'features': request_features
            },
        )
        print(response.status_code)
        print(response.json())
