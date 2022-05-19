FROM python:3.8.4-slim-buster

ADD app.py .

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT python app.py