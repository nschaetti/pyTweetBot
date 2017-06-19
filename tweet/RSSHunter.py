#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import feedparser

from tweet.Hunter import Hunter
from twitter.TweetGenerator import TweetGenerator
from .Tweet import Tweet


class RSSHunter(Hunter):

    # Constructor
    def __init__(self, url):
        self._feed_url = url
        self._entries = feedparser.parse(self._feed_url)['entries']
        self._current = 0
    # end __init__

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
        current_entry = self._entries[self._current]
        self._current += 1

        # Tweet generator
        #generator = TweetGenerator()
        #return generator(current_entry['title'], current_entry['links'][0]['href'])
        return Tweet(current_entry['title'], current_entry['links'][0]['href'])
    # end next

# end RSSHunter
