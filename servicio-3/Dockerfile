# FROM python:3.8

# EXPOSE 5000

# WORKDIR /app

# COPY requirements.txt /app
# RUN pip install -r requirements.txt

# COPY app.py /app
# CMD python app.py

FROM python:3.8.4-alpine

WORKDIR /code

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "flask","run" ]