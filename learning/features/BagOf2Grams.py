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


# Bag of 2 grams
class BagOf2Grams(object):
    """
    Bag of 2-grams
    """

    # Constructor
    def __init__(self, uppercase=False):
        """
        Constructor
        :param text:
        """
        self._uppercase = uppercase
    # end __init__

    #########################################
    # Public
    #########################################

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

        # Preceding token
        preceding_token = None

        # For each tokens
        for token in tokens:
            # Uppercase?
            if not self._uppercase:
                token = token.lower()
            # end if

            if preceding_token is None:
                preceding_token = token
            else:
                # Bigram
                bigram = preceding_token + u" " + token

                # Add
                try:
                    voc_count[bigram] += 1.0
                except KeyError:
                    voc_count[bigram] = 1.0
                # end try

                # Preceding token
                preceding_token = token
            # end if
        # end for

        return voc_count
    # end __call__

    #########################################
    # Private
    #########################################

# end BagOfWords
