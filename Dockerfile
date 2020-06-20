FROM python:3.7-stretch

RUN apt-get update && mkdir -p /app

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY /src/ /app/

ENV FLASK_APP "api.py"


