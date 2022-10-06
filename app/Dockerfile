FROM python:3.10.6-slim-buster

RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

COPY /app /usr/backend/app
WORKDIR /usr/backend
COPY requirements.txt .
COPY abi.json .
COPY .env .

RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /usr/backend/app/db
