FROM python:3.10-alpine

WORKDIR /code

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "flask","run" ]

# FROM python:3.8.4

# ADD app.py .

# COPY ./requirements.txt /requirements.txt

# RUN pip install --upgrade pip

# RUN pip install -r requirements.txt
# # CMD [ "python","./app.py" ]

# ENTRYPOINT python app.py