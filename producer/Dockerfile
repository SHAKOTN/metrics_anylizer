FROM python:3.8.3-alpine3.11 AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

RUN apk update && apk add bash

RUN pip install --upgrade pip

ADD producer/requirements/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN rm -f /app/requirements.txt

ADD producer /app/producer/
ADD producer_run.py /app/producer_run.py

WORKDIR /app

FROM base as test
ADD producer/requirements/requirements-test.txt /app/requirements-test.txt
RUN pip install -r /app/requirements-test.txt
RUN rm -f /app/requirements-test.txt
