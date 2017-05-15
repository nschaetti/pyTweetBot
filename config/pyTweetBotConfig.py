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

import json


class PyTweetBotConfig(object):

    def __init__(self, data):
        """
        Constructor.
        :param data:
        """
        self._database = data['database']
        self._twitter = data['twitter']
        self._friends = data['friends']
        self._direct_message = data['direct_message']
        self._news_settings = data['news_settings']
        self._news = data['news']
        self._retweet = data['retweet']
    # end __init__

    # Load configuration file.
    @staticmethod
    def load(config_file):
        """
        Load the configuration file
        :param config_file: Configuration filename.
        :return: PyTweetBotConfig object.
        """
        with open(config_file, 'r') as json_file:
            data = json.load(json_file)
        # end with
        return PyTweetBotConfig(data)
    # end load

    # Get database information.
    def get_database_config(self):
        """
        Get database information.
        :return: Database information
        """
        return self._database
    # end get_database_config

    # Get Twitter information.
    def get_twitter_config(self):
        """
        Get Twitter information.
        :return: Twitter information.
        """
        return self._twitter
    # end get_twitter_config

    # Get friends config.
    def get_friends_config(self):
        """
        Get friends config.
        :return:
        """
        return self._friends
    # end get_friends_config

    # Get Direct Message config
    def get_direct_message_config(self):
        """
        Get Direct Message information.
        :return:
        """
        return self._direct_message
    # end get_direct_message_config

    # Get news settings.
    def get_news_settings(self):
        """
        Get news settings.
        :return: News settings.
        """
        return self._news_settings
    # end get_news_settings

    # Get news config
    def get_news_config(self):
        """
        Get news config.
        :return: News config.
        """
        return self._news
    # end get_news_config

# end PyTweetBotConfig
