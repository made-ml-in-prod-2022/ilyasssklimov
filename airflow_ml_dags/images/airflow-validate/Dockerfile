FROM python:3.8
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY validate.py /validate.py
ENTRYPOINT ["python", "validate.py"]
