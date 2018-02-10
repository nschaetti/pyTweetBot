#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : CensorModel.py
# Description : pyTweetBot model keeping a list of forbidden words
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
from textblob import TextBlob, Word


# Forbidden words classifier
class CensorModel(object):
    """
    Forbidden words classifier
    """

    # Constructor
    def __init__(self, config):
        """
        Constructor
        :param config: Settings
        """
        # Forbidden words
        self._forbidden_words = config.forbidden_words

        # Extract
        self._forbidden_words = list()
        for word in config.forbidden_words:
            self._forbidden_words.append(Word(word.lower()).lemmatize())
        # end for
    # end __init__

    #################################################
    # Public
    #################################################

    #################################################
    # Override
    #################################################

    # Predict
    def __call__(self, x):
        """
        Predict
        :param x: Text to classify
        :return:
        """
        # Analyze text
        text_blob = TextBlob(x)
        print(text_blob.words)
        # For each forbidden word
        for word in text_blob.words:
            if Word(word.lower()).lemmatize() in self._forbidden_words:
                print(u"")
                print(u"NEG because of {}".format(word))
                exit()
                return 'neg', {'neg': 1.0, 'pos': 0.0}
            # end if
        # end for
        print(u"POS")
        return 'pos', {'neg': 0.0, 'pos': 1.0}
    # end __call__

    #################################################
    # Private
    #################################################

    #################################################
    # Static
    #################################################

    # Load a complete model and censor with path to model
    @staticmethod
    def load_censor(config):
        """
        Load a complete model and censor with path to model
        :param config:
        :return:
        """
        # Load model
        return CensorModel(config)
    # end load_model

# end Model
