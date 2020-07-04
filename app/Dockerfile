FROM ubuntu:18.04

MAINTAINER "krashilili0915@gmail.com"

# Setup work directory
RUN mkdir -p /usr/code/app
WORKDIR /usr/code/

# Install build essentials
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev redis-server build-essential libpq-dev locales netcat && \
    locale-gen en_US.UTF-8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'


# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


# Copy source code to /usr/code/app
COPY . app

# Copy manage.py and bash script to /usr/code
COPY manage.py entrypoint.sh ./

# Enable execution
RUN chmod +x ./entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/code/entrypoint.sh"]


