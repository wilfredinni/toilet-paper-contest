FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /django
COPY requirements/base.txt requirements/base.txt
COPY requirements/dev.txt requirements/dev.txt
COPY requirements/prod.txt requirements/prod.txt
RUN pip3 install -r requirements/dev.txt