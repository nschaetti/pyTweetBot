#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
from .TweetFactory import TweetFactory
from config.BotConfig import BotConfig


# Object representing a Tweet
class Tweet(object):
    """
    Object representing a Tweet.
    """

    # Constructor
    def __init__(self, text, url):
        """
        Constructor
        :param text: Tweet's text
        :param url: Tweet's URL
        """
        self._text = text
        self._url = url
    # end __init__

    ######################################
    #
    # Public function
    #
    ######################################

    # Get Tweet's text
    def get_text(self):
        """
        Get Tweet's text.
        :return: Tweet's text.
        """
        return self._text
    # end get_text

    # Set Tweet's text
    def set_text(self, text):
        """
        Set Tweet's text
        :param text:
        :return:
        """
        self._text = text
    # end set_text

    # Get Tweet's URL
    def get_url(self):
        """
        Get Tweet's URL
        :return: Tweet's URL
        """
        return self._url
    # end get_url

    # Set Tweet's URL
    def set_url(self, url):
        """
        Set Tweet's URL
        :param url:
        :return:
        """
        self._url = url
    # end set_url

    # Get Tweet
    def get_tweet(self):
        """
        Get Tweet
        :return: Complete Tweet's text
        """
        # Tweet Factory
        factory = TweetFactory(BotConfig().get_hashtags())

        # Create and return
        return factory(self)
    # end get_tweet

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        #print(self._text)
        return "Tweet(text={}, url={})".format(self._text, self._url)
    # end __str__

    # To unicode string
    def __unicode__(self):
        """
        To unicode string
        :return:
        """
        # print(self._text)
        return u"Tweet(text={}, url={})".format(self._text, self._url)
    # end __unicode__

# end Tweet
