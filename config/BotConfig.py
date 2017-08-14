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


# Bot config
class BotConfig(object):
    """
    Bot config
    """

    # Constructor
    def __init__(self, data=None):
        """
        Constructor.
        :param data:
        """
        self._database = data['database']
        self._twitter = data['twitter']
        self._friends = data['friends']
        self._direct_message = BotConfig.get_field(data, 'direct_message')
        self._news_settings = BotConfig.get_field(data, 'news_settings')
        self._news = BotConfig.get_field(data, 'news')
        self._retweet = BotConfig.get_field(data, 'retweet')
        self._hashtags = BotConfig.get_field(data, 'hashtags')
        self._rss = BotConfig.get_field(data, 'rss')
        self._forbidden_words = BotConfig.get_field(data, 'forbidden_words')
        self._email = data['email']
        self._scheduler_config = BotConfig.get_field(data, 'scheduler')
    # end __init__

    ######################################
    # Public
    ######################################

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
        return BotConfig(data)
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

    # Get hashtags
    def get_hashtags(self):
        """
        Get hashtags
        :return:
        """
        return self._hashtags
    # end get_hashtags

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

    # Get RSS streams
    def get_rss_streams(self):
        """
        Get RSS stream
        :return:
        """
        return self._rss
    # end get_rss_streams

    # Get news config
    def get_news_config(self):
        """
        Get news config.
        :return: News config.
        """
        return self._news
    # end get_news_config

    # Get forbidden words
    def get_forbidden_word(self):
        """
        Get forbidden words
        :return: Forbidden words
        """
        return self._forbidden_words
    # end get_forbidden_words

    # Get retweet settings
    def get_retweet_config(self):
        """
        Get retweet settings
        :return: Retweet settings
        """
        return self._retweet
    # end get_retweet_config

    # Get email address
    def get_email(self):
        """
        Get email
        :return:
        """
        return self._email
    # end get_email

    # Get scheduler config
    def get_scheduler_config(self):
        """
        Get scheduler config
        :return:
        """
        return self._scheduler_config
    # end get_scheduler_config

    ######################################
    # Private
    ######################################

    # Get a field
    @staticmethod
    def get_field(data, key):
        """
        Get a field
        :param data: Data
        :param key: Key of data
        :return: The value
        """
        try:
            return data[key]
        except KeyError:
            return []
        # end try
    # end _get_field

# end BotConfig
