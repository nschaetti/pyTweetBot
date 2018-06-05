#
# Dockerfile for pyTweetBot
#

FROM debian:latest
MAINTAINER Till Witt - witt@consider-it.de

RUN apt-get update
#RUN apt-get -y install libssl1.0-dev


# additional tools
RUN apt-get -y install git

#clone repository
RUN git clone https://github.com/nschaetti/pyTweetBot.git
WORKDIR /pyTweetBot

# Install Python package
RUN apt-get -y install python2.7
RUN apt-get -y install python-pip
RUN pip install simplejson
RUN pip install sqlalchemy
RUN pip install tweepy
RUN pip install feedparser
RUN pip install bs4
RUN pip install numpy
RUN pip install dnspython
RUN pip install sklearn
RUN pip install scipy
RUN pip install spacy
RUN pip install nltk
RUN pip install textblob


ENTRYPOINT /bin/bash
