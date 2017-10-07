#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
import db.obj
from .TweetFactory import TweetFactory


# Object representing a Tweet
class Tweet(object):
    """
    Object representing a Tweet.
    """

    # Constructor
    def __init__(self, text, url, hashtags=None, via=None):
        """
        Constructor
        :param text: Tweet's text
        :param url: Tweet's URL
        """
        self._factory = TweetFactory()
        self._text = self._factory(text)
        self._url = url
        self._hashtags = hashtags if hashtags is not None else list()
        self._via = via if via is not None else ""
    # end __init__

    ######################################
    # Public function
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
        # Text length
        text_length = len(self._text)

        # URL length
        url_length = 24
        if self._url == "":
            url_length = 0
        # end if

        # Total length
        total_length = text_length + url_length

        # Restrict text
        if total_length <= 140:
            final_text = self._text
        else:
            final_text = self._text[:140-total_length-3] + "..."
            total_length = len(final_text) + url_length
        # end if

        # Add via
        if total_length + 5 + len(self._via) <= 140 and self._via != "":
            final_text += " via " + self._via
            total_length += 5 + len(self._via)
        # end if

        # Add hashtags
        for hashtag in self._hashtags:
            if total_length + len(hashtag) <= 140:
                final_text += " " + hashtag
                total_length += len(hashtag)
            # end if
        # end for

        # Add URL
        final_text += " " + self._url

        # Create and return
        return final_text
    # end get_tweet

    # Get length
    def get_length(self):
        """
        Get Tweet length
        :return:
        """
        length = len(self._text)
        if self._url != "":
            length += 24
        # end if
        for hashtag in self._hashtags:
            length += len(hashtag)
        # end for
        if self._via != "":
            length += 5 + len(self._via)
        # end if
        return length
    # end get_length

    # Already tweeted
    def already_tweeted(self):
        """
        Already tweeted?
        :return: True/False
        """
        return db.obj.Tweeted.exists(self)
    # end already_tweeted

    ######################################
    # Override
    ######################################

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        return "Tweet(text={}, url={}, hashtags={}, via={}, length={})".format(self._text, self._url, self._hashtags,
                                                                               self._via, self.get_length())
    # end __str__

    # To unicode string
    def __unicode__(self):
        """
        To unicode string
        :return:
        """
        # print(self._text)
        return u"Tweet(text={}, url={}, hashtags={}, via={}, length={})".format(self._text, self._url, self._hashtags,
                                                                                self._via, self.get_length())
    # end __unicode__

# end Tweet
