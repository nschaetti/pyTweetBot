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
import random
import datetime
import logging
import time
from .default_config import default_config

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


# Field not available
class FieldNotAvailable(Exception):
    """
    Field is not available
    """
    pass
# end FieldNotAvailable


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
            'email': False,
            'scheduler': False,
            'hashtags': False,
            'twitter': True,
            'friends': False,
            'forbidden_words': False,
            'direct_message': False,
            'news_settings': False,
            'news': False,
            'rss': False,
            'retweet': False,
            'github': False
        }

        # Settings available
        for key in self._required_states:
            if self._required_states[key] and key not in data:
                raise MissingRequiredField(u"The required field {} is missing in configuration file".format(key))
            # end if
        # end for

        # Set
        self._config = data
    # end __init__

    ######################################
    # Property
    ######################################

    # Get database settings
    @property
    def database(self):
        """
        Get database settings
        :return: Database settings (username, password, database)
        """
        return self['database']
    # end database_config

    # Get Twitter settings
    @property
    def twitter(self):
        """
        Get Twitter settings
        :return:
        """
        return self['twitter']
    # end twitter

    # Get friends settings
    @property
    def friends(self):
        """
        Get friends settings
        :return:
        """
        return self['friends']
    # end friends

    # Get hashtags settings
    @property
    def hashtags(self):
        """
        Get hashtags settins
        :return:
        """
        return self['hashtags']
    # end hashtags

    # Get direct message config
    @property
    def direct_message(self):
        """
        Get direct message config
        :return:
        """
        return self['direct_message']
    # end direct_message

    # Get tweet settings
    def tweet(self):
        """
        Get tweet settings
        :return:
        """
        return self['tweet']
    # end tweet

    ######################################
    # Public
    ######################################

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

    # Is setting available
    def is_available(self, key):
        """
        Is setting available?
        :param key:
        :return:
        """
        return key in self._config
    # end is_available

    # Get a random waiting time
    def get_random_waiting_time(self):
        """
        Get a random waiting time
        :return:
        """
        try:
            (min_time, max_time) = self._scheduler_config['waiting_times']
        except KeyError:
            (min_time, max_time) = self._default_value['waiting_times']

        # Return random waiting time
        return random.randint(min_time * 60, max_time * 60)
    # end get_random_waiting_time

    # Wait between action
    def wait_next_action(self):
        """
        Wait next action
        :return:
        """
        # Waiting time
        waiting_seconds = self.get_random_waiting_time()

        # Log
        logging.getLogger(u"pyTweetBot").info(
            u"Waiting {0:.{1}f} minutes for next run".format(waiting_seconds / 60.0, 1))

        # Wait
        time.sleep(waiting_seconds)
    # end wait_next_action

    # Is the scheduler awake
    def is_awake(self):
        """
        Is the scheduler awake
        :return:
        """
        # Sleep time
        try:
            (sleep_time, wake_time) = self._scheduler_config['sleep']
        except KeyError:
            (sleep_time, wake_time) = self._default_value['sleep']
        # end try

        # Now
        now_time = datetime.datetime.utcnow()

        # Asleep
        return now_time.hour < sleep_time or now_time.hour > wake_time
    # end is_awake

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

    # Get field default value
    def _get_default_value(self, key, subkey=None):
        """
        Get field default value
        :param key:
        :param subkey:
        :return:
        """
        pass
    # end _get_default_value

    ######################################
    # Override
    ######################################

    # Get settings
    def __getitem__(self, item):
        """
        Get settings
        :param item:
        :return:
        """
        return self._config[item]
    # end __getitem__

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
