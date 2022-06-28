FROM python:3.8
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY train.py /train.py
ENTRYPOINT ["python", "train.py"]
