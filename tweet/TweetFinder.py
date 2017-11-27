#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : TweetFinder.py
# Description : Tweet finder object.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 16.10.2017 22:28:00
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

from .Hunter import Hunter
import random
import logging


# Find new tweets from a set of
# sources (Google News, RSS)
class TweetFinder(Hunter):
    """
    Find new tweets from a set of
    sources (Google News, RSS)
    """

    # Constructor
    def __init__(self, shuffle=False, tweet_factory=None):
        """
        Constructor
        :param shuffle: Shuffle hunters before iterating?
        :param tweet_factory: The tweet factory object
        """
        self._hunters = list()
        self._current = 0
        self._n_hunters = 0
        self._shuffle = shuffle
        self._tweet_factory = tweet_factory
        self._classifiers = list()
    # end __init__

    ######################################################
    # PUBLIC FUNCTIONS
    ######################################################

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

    # Set the tweet factory
    def set_factory(self, tweet_factory):
        """
        Set the tweet factory
        :param tweet_factory: The tweet facgory
        """
        self._tweet_factory = tweet_factory
    # end set_factory

    # Set classifier
    def add_classifier(self, classifier):
        """
        Add a classifier
        :param classifier:
        """
        self._classifiers.append(classifier)
    # end add_classifier

    ######################################################
    # PRIVATE
    ######################################################

    # Generate the tweet
    def _to_the_factory(self, tweet_text):
        """
        Generate the tweet
        :param tweet_text: Text to transform
        :return: The transformed text by factory
        """
        if self._tweet_factory is not None:
            return self._tweet_factory(tweet_text)
        # end if
        return tweet_text
    # end _to_the_factory

    ######################################################
    # OVERRIDE
    ######################################################

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
        if self._current >= self._n_hunters:
            raise StopIteration
        else:
            try:
                return self._to_the_factory(self._hunters[self._current].next())
            except StopIteration:
                self._current += 1
                if self._current < self._hunters:
                    logging.getLogger(u"pyTweetBot").info(u"Changing hunter to {}".format(self._hunters[self._current]))
                # end if
                return self._to_the_factory(self.next())
            # end try
        # end if
    # end next

# end TweetFinder
