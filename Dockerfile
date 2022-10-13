FROM python:3.10.7-alpine

RUN pip install --upgrade pip
WORKDIR /var/docker-python

COPY requirements.txt /var/docker-python/requirements.txt

RUN pip install -r requirements.txt