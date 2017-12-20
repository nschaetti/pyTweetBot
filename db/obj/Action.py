#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Action.py
# Description : pyTweetBot Action in the DB.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
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
from sqlalchemy import Column, String, BigInteger, DateTime, Enum
from .Base import Base
from pyTweetBot.twitter
from pyTweetBot.friends
from db.obj.Tweeted import Tweeted


# Action
class Action(Base):
    """
    Action
    """

    # Table name
    __tablename__ = "pytwb_actions"

    # Fields
    action_id = Column(BigInteger, primary_key=True)
    action_type = Column(Enum('Tweet', 'Retweet', 'Like', 'DirectMessage', 'Follow', 'Unfollow'), nullable=False)
    action_order = Column(BigInteger, nullable=False)
    action_tweet_id = Column(BigInteger, nullable=True)
    action_tweet_text = Column(String(5000), nullable=True)
    action_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())

    ############################################
    # Public Functions
    ############################################

    # Execute the action
    def execute(self):
        """
        Execute the action
        :return:
        """
        if self.action_type == "Follow":
            # Follow
            pyTweetBot.friends.FriendsManager().follow(self.action_tweet_text)
        elif self.action_type == "Unfollow":
            # Unfollow
            pyTweetBot.friends.FriendsManager().unfollow(self.action_tweet_text)
        elif self.action_type == "Like":
            # Like
            pyTweetBot.twitter.TweetBotConnector().like(self.action_tweet_id)
            Tweeted.insert_retweet(self.action_tweet_id, self.action_tweet_text)
        elif self.action_type == "Tweet":
            # Tweet
            pyTweetBot.twitter.TweetBotConnector().tweet(self.action_tweet_text)
            Tweeted.insert_tweet(self.action_tweet_text)
        elif self.action_type == "Retweet":
            # Retweet
            pyTweetBot.twitter.TweetBotConnector().retweet(self.action_tweet_id)
            Tweeted.insert_retweet(self.action_tweet_id, self.action_tweet_text)
        # end if
    # end

    ############################################
    # Static functions
    ############################################

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        return "Action(id={}, type={}, tweet_id={}, tweet_text={}, tweet_date={})".format(
            self.action_id,
            self.action_type,
            self.action_tweet_id,
            self.action_tweet_text,
            self.action_date)
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"Action(id={}, type={}, tweet_id={}, tweet_text={}, tweet_date={})".format(
            self.action_id,
            self.action_type,
            self.action_tweet_id,
            self.action_tweet_text,
            self.action_date)
    # end __unicode__

# end Action
