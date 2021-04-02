FROM python:3.8-alpine3.12
RUN apk update && apk upgrade && apk add bash && apk add supervisor
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip
RUN mkdir /app_in_docker
WORKDIR /app_in_docker
COPY . /app_in_docker/
RUN pip install -r requirements.txt
EXPOSE 1883
