#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import feedparser
from .Hunter import Hunter
from twitter.TweetGenerator import TweetGenerator
from .Tweet import Tweet
import logging
import time
import re
from twitter.TweetBotConnect import TweetBotConnector
from textblob import TextBlob
from news.GoogleNewsClient import GoogleNewsClient
import tools


# Find new tweets from Twitter researches
class TwitterHunter(Hunter):
    """
    Find new tweets from Twitter researches
    """

    # Constructor
    def __init__(self, search_term, hashtags, n_pages=2, polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        :param hashtag: Hashtag
        """
        self._search_term = search_term
        self._hashtags = hashtags
        self._cursor = TweetBotConnector().search_tweets(search_term, n_pages)
        self._current = 0
        self._tweets = list()
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages
    # end __init__

    # Get hashtags
    def get_hashtags(self):
        """
        Get hashtag
        """
        return self._hashtags
    # end get_stream

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"TwitterHunter(hashtag={})".format(self._search_term)
    # end __unicode__

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
        Next
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
            # Get urls
            urls = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", tweet.text)

            # If there is URLs in the tweet
            if len(urls) > 0:
                # Analyze text
                tweet_blob = TextBlob(tweet.text)
                # Pass level of pol & sub
                if tweet_blob.sentiment.polarity >= self._polarity and \
                                tweet_blob.sentiment.subjectivity <= self._subjectivity and \
                                tweet_blob.detect_language() in self._languages:
                    # Retrieve page
                    page_parser = tools.PageParser(urls[0])

                    # Add to tweets
                    self._tweets.append(Tweet(page_parser.title, urls[0], self._hashtags))
                # end if
            # end if
        # end for

        # Wait
        logging.getLogger(u"pyTweetBot").info(u"Waiting 60 seconds...")
        time.sleep(60)
    # end _load_tweets

# end RSSHunter
