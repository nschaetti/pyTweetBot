#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Action.py
# Description : pyTweetBot Tweet in the DB.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 28.07.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, or_
from .Base import Base
import tweet as tw
from db.DBConnector import DBConnector


# Tweet
class Tweeted(Base):
    """
    Tweet
    """

    # Table name
    __tablename__ = "pytwb_tweets"

    # Fields
    tweet_id = Column(BigInteger, primary_key=True)
    tweet_tweet_id = Column(BigInteger, nullable=True)
    tweet_tweet_text = Column(String(5000), nullable=True)
    tweet_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    ############################################
    # Public Functions
    ############################################

    # Insert a new tweeted
    @staticmethod
    def insert_tweet(tweet_text):
        """
        Insert a new tweeted
        :param tweet_text: Tweet's text
        :return:
        """
        DBConnector().get_session().add(Tweeted(tweet_tweet_text=tweet_text))
    # end insert_tweet

    # Insert a new retweeted
    @staticmethod
    def insert_retweet(tweet_id, tweet_text):
        """
        Insert a new retweeted
        :param tweet_id: Tweet's ID
        :param tweet_text: Tweet's text
        """
        DBConnector().get_session().add(Tweeted(tweet_tweet_id=tweet_id, tweet_tweet_text=tweet_text))
    # end insert_tweet

    # Tweet exists
    @staticmethod
    def exists(tweet):
        if tweet is tw.Tweet:
            return DBConnector().get_session().query(Tweeted).filter(
                or_(Tweeted.tweet_tweet_text == tweet.get_text(),
                    Tweeted.tweet_tweet_url == tweet.get_url())).count() > 0
        elif tweet is unicode:
            return DBConnector().get_session().query(Tweeted).filter(Tweeted.tweet_tweet_text == tweet).count() > 0
        elif tweet is int:
            return DBConnector().get_session().query(Tweeted).filter(Tweeted.tweet_tweet_id == tweet).count() > 0
        # end if
    # end exists

# end Action
