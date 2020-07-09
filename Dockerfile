FROM python:3.7

RUN apt-get update && apt-get install -y --no-install-recommends \
  python3.7 \ 
  python3-pip \
  python3-flask
#  python3.7-venv

RUN mkdir -p /app

COPY src /app/
COPY requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt --upgrade
RUN pip3 install setuptools --upgrade

ENV FLASK_APP=src/api.py
ENV FLASK_DEBUG=1
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

