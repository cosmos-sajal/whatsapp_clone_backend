FROM python:3.8.3-slim-buster
MAINTAINER github.com/cosmos-sajal

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    libcurl4-openssl-dev \
    libssl-dev \
    mime-support \
    postgresql-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && apt-get install -y libcurl4-openssl-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY ./app /app
COPY ./serviceAccount.json /
