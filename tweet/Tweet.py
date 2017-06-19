#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


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

    # Get Tweet's URL
    def get_url(self):
        """
        Get Tweet's URL
        :return: Tweet's URL
        """
        return self._url
    # end get_url

# end Tweet
