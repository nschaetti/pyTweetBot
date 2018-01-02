#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import pyTweetBot
from textblob import TextBlob
import time
import logging


# Class to find tweet to retweet
class RetweetFinder(object):
    """
    Class to find tweet to retweet
    """

    # Constructor
    def __init__(self, search_keywords="", n_pages=-1, polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        """
        # Properties
        self._search_keywords = search_keywords
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages

        # Cursor
        if search_keywords == "":
            self._cursor = pyTweetBot.twitter.TweetBotConnector().get_time_line(n_pages)
        else:
            self._cursor = pyTweetBot.twitter.TweetBotConnector().search_tweets(search_keywords, n_pages)
        # end if

        # Current list of tweets
        self._tweets = list()
    # end __init__

    #############################################
    # Override
    #############################################

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return:
        """
        return self
    # end __iter__

    # Next
    def next(self):
        """
        Next element
        :return:
        """
        # Load if needed
        while len(self._tweets) == 0:
            self._load_tweets()
        # end if

        # Current tweet
        current_tweet = self._tweets[0]

        # Remove
        self._tweets.remove(current_tweet)

        # Return
        return current_tweet
    # end next

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"RetweetFinder({})".format(self._search_keywords)
    # end __unicode__

    # To str
    def __str__(self):
        """
        To str
        :return:
        """
        return "RetweetFinder({})".format(self._search_keywords)
    # end __str__

    ############################################
    # Private
    ############################################

    # Get tweets
    def _load_tweets(self):
        """
        Get tweets
        :return: A tweet
        """
        # Get page
        page = self._cursor.next()

        # Get all tweets
        for tweet in page:
            # if not tweet.retweeted and 'RT @' not in tweet.text:
            if not tweet.retweeted:
                # Analyze text
                tweet_blob = TextBlob(tweet.text)

                # Pass level of pol & sub
                if tweet_blob.sentiment.polarity >= self._polarity and \
                    tweet_blob.sentiment.subjectivity <= self._subjectivity and \
                    tweet_blob.detect_language() in self._languages:
                    self._tweets.append((tweet, tweet_blob.sentiment.polarity, tweet_blob.sentiment.subjectivity))
                # end if
        # end for

        # Wait
        logging.getLogger(u"pyTweetBot").info(u"Waiting 60 seconds...")
        time.sleep(60)
    # end _load_tweets

# end TweetFinder
