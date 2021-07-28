FROM python:3.8

RUN mkdir /code

WORKDIR /code
ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ./src src

WORKDIR /code/src