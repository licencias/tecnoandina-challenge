FROM python:3.8.4-slim-buster

ADD app.py .

RUN pip install --upgrade pip

RUN pip install paho-mqtt

ENTRYPOINT python app.py