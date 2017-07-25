#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from .Hunter import Hunter
import random
from textblob import TextBlob


class TweetFinder(Hunter):

    # Constructor
    def __init__(self, shuffle=False, polarity=0.0, subjectivity=0.5, languages=['en']):
        """
        Constructor
        """
        self._hunters = list()
        self._current = 0
        self._n_hunters = 0
        self._shuffle = shuffle
        self._polarity = polarity
        self._subjectivity = subjectivity
        self._languages = languages
    # end __init__

    # Add an hunter
    def add(self, hunter):
        """
        Add an hunter to the list
        :param hunter:
        :return:
        """
        self._hunters.append(hunter)
        self._n_hunters += 1
        if self._shuffle:
            random.shuffle(self._hunters)
        # end if
    # end add

    # Remove hunter
    def remove(self, hunter):
        """
        Remove hunter
        :param hunter:
        :return:
        """
        self._hunters.remove(hunter)
        self._n_hunters -= 1
    # end remove

    # Iterator
    def __iter__(self):
        return self
    # end __iter__

    # Next
    def next(self):
        """
        Next element
        :return:
        """
        if self._current >= self._n_hunters:
            raise StopIteration
        else:
            try:
                return self._hunters[self._current].next()
            except StopIteration:
                self._current += 1
                """if self._current >= self._n_hunters:
                    raise StopIteration
                else:
                    return self._hunters[self._current].next()
                # end if"""
                return self.next()
            # end try
        # end if
    # end next

# end TweetFinder
