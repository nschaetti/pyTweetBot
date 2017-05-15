#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot action in the DB.
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
import MySQLdb as mdb


# pyTweetBot class for actions
# contained in the DB.
class PyTweetBotAction(object):
    """
    pyTweetBot class for actions contained in the DB.
    """

    # Constructor
    def __init__(self, tweet_id, text, exec_date):
        """
        Constructor
        :param tweet_id: Tweet's ID (like, retweet).
        :param text: Tweet's text (tweet).
        :param exec_date: Date of execution.
        """
        self._id = -1
        self._tweet_id = tweet_id
        self._text = text
        self._exec_date = exec_date
    # end __init__

    # Insert
    def insert(self):
        pass
    # end insert

# end pyTweetBot