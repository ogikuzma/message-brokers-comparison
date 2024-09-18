FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt update && apt install -y wget

RUN wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0.amd64.deb
RUN dpkg -i rocketmq-client-cpp-2.0.0.amd64.deb