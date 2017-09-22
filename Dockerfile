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

RUN git clone https://github.com/nschaetti/nsNLP.git


RUN apt-get -y install python3
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

RUN git clone https://github.com/nschaetti/Oger.git

RUN pip install mdp

RUN pip install  matplotlib
RUN apt-get -y install python-tk
RUN pip install nltk
RUN pip install textblob
#RUN pip install
#RUN pip install
#RUN pip install
#RUN pip install
#RUN pip install
#RUN pip install
#RUN pip install
#RUN pip install


ENTRYPOINT /bin/bash
