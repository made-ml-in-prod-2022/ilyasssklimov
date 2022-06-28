FROM python:3.8
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY ./models/model.pkl /model.pkl
COPY app.py /app.py

WORKDIR .

ENV PATH_TO_MODEL="/model.pkl"

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]