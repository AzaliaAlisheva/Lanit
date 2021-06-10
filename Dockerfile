# Install base Python image
FROM python:3.8-slim-buster

# Copy files to the container
COPY *.py /app/
COPY requirements.txt /app/

# Set working directory to previously added app directory
WORKDIR /app/

# Install dependencies
RUN apt-get install g++

RUN pip install -r requirements.txt
RUN apt-get install gzip
RUN apt-get update
RUN apt-get install build-essential -y
RUN apt-get install wget -y
RUN pip install fasttext

RUN wget https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ru.300.bin.gz
