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
import random
import time
from sqlalchemy import Column, String, BigInteger, DateTime, Enum
from .Base import Base
from twitter.TweetBotConnect import TweetBotConnector
from friends.FriendsManager import FriendsManager
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
    action_type = Column(Enum('Tweet', 'Retweet', 'Like', 'DirectMessage', 'FollowUnfollow'), nullable=False)
    action_order = Column(BigInteger, nullable=False)
    action_tweet_id = Column(BigInteger, nullable=True)
    action_tweet_text = Column(String(5000), nullable=True)
    action_follow = Column(String(100), nullable=True)
    action_unfollow = Column(String(100), nullable=True)
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
        if self.action_type == "FollowUnfollow":
            # Follow
            FriendsManager().follow(self.action_follow)

            # Wait between 10 and 30 seconds
            time.sleep(random.randint(10, 30))

            # Unfollow
            FriendsManager().unfollow(self.action_unfollow)
        elif self.action_type == "Like":
            TweetBotConnector().like(self.action_tweet_id)
            Tweeted.insert_retweet(self.action_tweet_id, self.action_tweet_text)
        elif self.action_type == "Tweet":
            TweetBotConnector().tweet(self.action_tweet_text)
            Tweeted.insert_tweet(self.action_tweet_text)
        elif self.action_type == "Retweet":
            TweetBotConnector().retweet(self.action_tweet_id)
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
        return "Action(id={}, type={}, tweet_id={}, tweet_text={}, action_follow={}, action_unfollow={}, tweet_date={})".format(
            self.action_id,
            self.action_type,
            self.action_tweet_id,
            self.action_tweet_text,
            self.action_follow,
            self.action_unfollow,
            self.action_date)
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"Action(id={}, type={}, tweet_id={}, tweet_text={}, action_follow={}, action_unfollow={}, tweet_date={})".format(
            self.action_id,
            self.action_type,
            self.action_tweet_id,
            self.action_tweet_text,
            self.action_follow,
            self.action_unfollow,
            self.action_date)
    # end __unicode__

# end Action
