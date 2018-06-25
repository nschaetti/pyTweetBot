#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import feedparser
from .Hunter import Hunter
from .Tweet import Tweet
import logging
from textblob import TextBlob


# Find new tweets from RSS streams
class RSSHunter(Hunter):
    """
    Find new tweets from RSS streams
    """

    # Constructor
    def __init__(self, stream):
        self._stream = stream
        self._stream_url = stream['url']
        logging.debug(u"Retreiving RSS stream {}".format(self._stream_url))
        self._entries = feedparser.parse(self._stream_url)['entries']
        self._hashtags = stream['hashtags'] if 'hashtags' in stream else list()
        self._lang = stream['lang']
        self._current = 0
    # end __init__

    # Get stream
    def get_stream(self):
        """
        Get stream
        """
        return self._stream
    # end get_stream

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"RSSHunter(stream={})".format(self._stream)
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
        if self._current >= len(self._entries):
            raise StopIteration
        # end if

        # Found
        found = False

        while not found or self._current < len(self._entries):
            # Get current entry
            current_entry = self._entries[self._current]

            # Analyze text
            tweet_blob = TextBlob(current_entry['title'])
            print(tweet_blob)
            # Right language
            if tweet_blob.detect_language() == self._lang:
                found = True
            # end if

            # Next
            self._current += 1
        # end while

        # Tweet generator
        if found:
            return Tweet(current_entry['title'], current_entry['links'][0]['href'], self._hashtags)
        else:
            raise StopIteration
        # end if
    # end next

# end RSSHunter
