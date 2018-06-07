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
from .required_fields import required_fields


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

# This class reads the JSON configuration file and
# check that all required field is set.
# It will check that a field a available when
# asked for or will raise a FieldNotAvailable exception.
class BotConfig(object):
    """This class reads the JSON configuration file and
    check that all required field is set.
    It will check that a field a available when
    asked for or will raise a FieldNotAvailable exception.

    .. note:
        Simple note

    Arguments:
        data (dict): Configuration data as a dictionary.
    """

    # Constructor
    def __init__(self, data):
        """
        Constructor
        :param data: Settings read from JSON file as a dictionary
        """
        # Check required fields
        config_ok, missing_field = self._check_config(data)
        if not config_ok:
            raise MissingRequiredField(u"The required field {} is missing in configuration file".format(missing_field))
        # end if

        # Set
        self._config = data
    # end __init__

    ######################################
    # Property
    ######################################

    # Get database settings
    @property
    def database(self):
        """Get database settings

        Returns:
            Database settings (username, password, database)
        """
        return self['database']
    # end database_config

    # Get Twitter settings
    @property
    def twitter(self):
        """Get Twitter settings

        Returns:
            Twitter settings (tokens)
        """
        return self['twitter']
    # end twitter

    # Get friends settings
    @property
    def friends(self):
        """Get friends settings

        Returns:
            Friends settings
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
    @property
    def tweet(self):
        """
        Get tweet settings
        :return:
        """
        return self['tweet']
    # end tweet

    # Get RSS streams
    @property
    def rss(self):
        """
        Get RSS streams
        :return:
        """
        return self['rss']
    # end rss

    # Get Google News settings
    @property
    def google_news(self):
        """
        Get Google News settings
        :return:
        """
        return self['news']
    # end google_news

    # Get forbidden words
    @property
    def forbidden_words(self):
        """
        Get forbidden words
        :return:
        """
        return self['forbidden_words']
    # end forbidden_words

    # Get retweet settings
    @property
    def retweet(self):
        """
        Get retweet settings
        :return:
        """
        return self['retweet']
    # end retweet

    # Get email address
    @property
    def email(self):
        """
        Get email address
        :return:
        """
        return self['email']
    # end email

    # Get scheduler config
    @property
    def scheduler(self):
        """
        Get scheduler config
        :return:
        """
        return self['scheduler']
    # end scheduler

    # Get GitHub config
    @property
    def github(self):
        """
        Get GitHub config
        :return:
        """
        return self['github']
    # end github

    ######################################
    # Public
    ######################################

    # Is setting available
    def is_available(self, key):
        r"""Is a setting available in the loaded configuration?

        Arguments:
            key: Setting's key in the configuration

        Returns:
        """
        """
        Is setting available?
        :param key: Key to check the availability
        :return: True if available, False otherwise
        """
        return key in self._config
    # end is_available

    # Get a random interval
    def get_random_interval(self, setting):
        r"""Get a random waiting time for a specific type of actions.

        Arguments:
            setting: Setting type. Can be tweet, retweet, like, follow, unfollow

        Returns:
                A time interval as an integer corresponding to the time in seconds.
        """
        # Setting type str or unicode
        assert isinstance(setting, str) or isinstance(setting, unicode)

        # Which action type
        if setting == "tweet":
            (min_time, max_time) = self.get_current_interval(self.tweet)
        elif setting == "retweet" or setting == "like":
            (min_time, max_time) = self.get_current_interval(self.retweet)
        elif setting == "follow" or setting == "unfollow":
            (min_time, max_time) = self.get_current_interval(self.friends)
        # end if

        # Unfollow
        if setting == "unfollow":
            min_time -= 5
            max_time -= 5
        # end if

        # Return random waiting time
        return random.randint(min_time * 60, max_time * 60)
    # end get_random_waiting_time

    # Get current interval
    def get_current_interval(self, setting):
        """
        Get current interval
        :param setting:
        :return:
        """
        if 'intervals' in setting.keys():
            # For each intervals
            for interval in setting['intervals']:
                day = interval['day']
                start = interval['start']
                end = interval['end']
                now = datetime.datetime.now()
                if now.weekday() == day and now.hour >= start and now.hour <= end:
                    return interval['interval']
                # end if
            # end for
        # end if

        return setting['interval']
    # end get_current_interval

    # Wait between action
    def wait_next_action(self, setting):
        """
        Wait next action
        :param setting: Setting type (tweet, retweet, friend)
        """
        # Waiting time
        waiting_seconds = self.get_random_interval(setting)

        # Log
        logging.getLogger(u"pyTweetBot").info(
            u"Waiting {0:.{1}f} minutes for next run of {2}".format(waiting_seconds / 60.0, 1, setting))

        # Wait
        time.sleep(waiting_seconds)
    # end wait_next_action

    # Is the scheduler awake?
    def is_awake(self):
        """
        Is the scheduler awake?
        :return: True if awake, False otherwise
        """
        # Sleep time
        try:
            (sleep_time, wake_time) = self.scheduler['sleep']
        except KeyError:
            return True
        # end try

        # Now
        now_time = datetime.datetime.utcnow()

        # Asleep
        return now_time.hour < sleep_time or now_time.hour > wake_time
    # end is_awake

    ######################################
    # Private
    ######################################

    # Check if required fields are available
    def _check_config(self, data):
        """
        Check if required field are available
        :param data: Setting dictionary
        :param required_fields: Dictionary of required fields
        :return: True if required field present, False otherwise
        """
        for key in required_fields.keys():
            if key not in data.keys():
                return False, key
            else:
                self._check_config(data[key])
            # end if
        # end for
        return True, None
    # end _check_config

    ######################################
    # Override
    ######################################

    # Get a setting item
    def __getitem__(self, item):
        """
        Get setting item
        :param item: Setting key
        :return: The setting value
        """
        try:
            return self._config[item]
        except KeyError:
            if item not in default_config.keys():
                raise FieldNotAvailable(u"The required field {} is not available in configuration file".format(item))
            else:
                return default_config[item]
            # end if
        # end try
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
