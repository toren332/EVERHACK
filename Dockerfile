FROM python:3.8

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/