#FROM debian:buster-slim
FROM ubuntu:17.10

LABEL maintainer="Till Witt <witt@consider-it.de>"

RUN apt-get update && \
    apt-get -y install python2.7 python-pip libmariadbclient-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/*

ADD ./ /app
WORKDIR /app

RUN pip install -r requirements.txt
ENV PYTHONIOENCODING "utf-8"

CMD /bin/bash
