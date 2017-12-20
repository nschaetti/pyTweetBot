#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Classifier.py
# Description : Classifier base class
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

# Import packages


# Bag of Grams
class BagOfGrams(object):
    """
    Bag of Grams
    """

    # Constructor
    def __init__(self, uppercase=False):
        """
        Constructor
        :param text:
        """
        self._uppercase = uppercase
        self._bows = list()
    # end __init__

    #########################################
    # Public
    #########################################

    # Add features
    def add(self, bow):
        """
        Add features
        :param bow:
        :return:
        """
        self._bows.append(bow)
    # end add

    #########################################
    # Override
    #########################################

    # Call
    def __call__(self, tokens):
        """
        Call
        :return:
        """
        # Vocabulary
        voc_count = dict()

        # For each features
        for bow in self._bows:
            # Get features
            features = bow(tokens)

            # For each token
            for token in features.keys():
                try:
                    voc_count[token] += features[token]
                except KeyError:
                    voc_count[token] = features[token]
                # end
            # end for
        # end for

        return voc_count
    # end __call__

    #########################################
    # Private
    #########################################

# end BagOfGrams
