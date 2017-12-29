#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : stats.TweetStatistics.py
# Description : pyTweetBot tweet statistics managing class.
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

# Imports
import logging
from pyTweetBot.db.DBConnector import DBConnector
from pyTweetBot.executor.ActionScheduler import ActionScheduler
from pyTweetBot.db.obj.Statistic import Statistic
from pyTweetBot.patterns.singleton import singleton
from pyTweetBot.twitter.TweetBotConnect import TweetBotConnector
from pyTweetBot.friends.FriendsManager import FriendsManager
from sqlalchemy import update, delete, select
from sqlalchemy.orm import load_only
from sqlalchemy import or_, and_, not_


#######################################
# Class
#######################################


# Manage user's statistics
@singleton
class UserStatistics(object):
    """
    Manage user's statistics
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        # DB session
        self._session = DBConnector().get_session()

        # Twitter connection
        self._twitter_con = TweetBotConnector()

        # Friends manager
        self._friend_manager = FriendsManager()

        # Logger
        self._logger = logging.getLogger(name="pyTweetBot")
    # end __init__

    #################################################
    # Public
    #################################################

    # Insert a value in the statistics table
    def update_statistics(self):
        """
        Insert a value in the statistics table.
        """
        # Stats
        n_followers = self._friend_manager.n_followers
        n_following = self._friend_manager.n_followings
        n_statuses = ActionScheduler().n_statuses()

        # Add
        statistic = Statistic(statistic_friends_count=n_following,
                              statistic_followers_count=n_followers,
                              statistic_statuses_count=n_statuses)
        self._session.add(statistic)
        self._session.commit()

        return n_followers, n_following, n_statuses
    # end update_statistics

    # Get statistics
    def get_statistics(self):
        """
        Get statistics
        :return:
        """
        return self._session.query(Statistic).order_by(Statistic.statistic_date)
    # end get_statistics

    # Get last inserted statistics
    def get_last_statistics(self, pos=-1):
        """
        Get last inserted statistics
        :param pos:
        :return:
        """
        # Get statistics
        statistics = self.get_statistics()

        # Return
        return statistics[pos]
    # end get_last_statistics

# end UserStatistics
