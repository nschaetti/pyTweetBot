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

# Imports
import simplejson

#############################################
# Exceptions
#############################################


# Exception raised when a required field is missing
class MissingRequiredField(Exception):
    """
    Exception raised when a required field is missing
    """
    pass
# end MissingRequiredField


#############################################
# CLASS
#############################################

# Read, parse and store configuration informations
class BotConfig(object):
    """
    Read, parse and store configuration informations
    """

    # Constructor
    def __init__(self, data):
        """
        Constructor.
        :param data: Dictionary containing settings
        """
        # Required states
        self._required_states = \
        {
            'database': True,
            'twitter': True,
            'friends': False,
            'direct_message': False,
            'news_settings': False,
            'news': False,
            'retweet': False,
            'hashtags': False,
            'rss': False,
            'forbidden_words': False,
            'email': False,
            'scheduler': False,
            'github': False
        }

        # Settings available
        self._availability = dict()
        for key in self._required_states:
            self._availability[key] = False
        # end for

        # Load
        self._database = data['database']
        self._twitter = data['twitter']
        self._friends = data['friends']
        self._direct_message = self._get_field(data, 'direct_message')
        self._news_settings = self._get_field(data, 'news_settings')
        self._news = self._get_field(data, 'news')
        self._retweet = self._get_field(data, 'retweet')
        self._hashtags = self._get_field(data, 'hashtags')
        self._rss = self._get_field(data, 'rss')
        self._forbidden_words = self._get_field(data, 'forbidden_words')
        self._email = data['email']
        self._scheduler_config = self._get_field(data, 'scheduler')
        self._github_config = data['github']
    # end __init__

    ######################################
    # Public
    ######################################

    # Get database settings
    @property
    def database_settings(self):
        """
        Get database settings
        :return: Database settings (username, password, database)
        """
        return self._database
    # end database_config

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
    def get_forbidden_words(self):
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

    # Get github config
    def get_github_config(self):
        """
        Get GitHub config
        :return:
        """
        return self._github_config
    # end get_github_config

    ######################################
    # Private
    ######################################

    # Get a field
    def _get_field(self, data, key, required=False):
        """
        Get a field
        :param data: Data
        :param key: Key of data
        :return: The value
        """
        try:
            self._availability[key] = True
            return data[key]
        except KeyError:
            if not required:
                self._availability[key] = False
                return []
            else:
                raise MissingRequiredField(u"The required field {} is missing in configuration file".format(key))
            # end if
        # end try
    # end _get_field

    ######################################
    # Static
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
            data = simplejson.load(json_file)
        # end with
        return BotConfig(data)
    # end load

# end BotConfig
