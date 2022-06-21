FROM python:3.8
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY generate.py /generate.py
ENTRYPOINT ['python3', 'generate.py']
