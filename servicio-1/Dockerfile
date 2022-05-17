FROM python:3.8.4-slim-buster

ADD app.py .

RUN pip install paho-mqtt

# CMD [ "python","./app.py" ]

ENTRYPOINT python app.py