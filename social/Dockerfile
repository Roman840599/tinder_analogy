FROM python:3.8-alpine3.12
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN mkdir /app_in_docker
WORKDIR /app_in_docker
COPY . /app_in_docker/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
