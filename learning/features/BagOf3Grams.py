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


# Bag of 3 grams
class BagOf3Grams(object):
    """
    Bag of 3-grams
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

        # Preceding tokens
        last_token1 = None
        last_token2 = None

        # For each tokens
        for token in tokens:
            # Uppercase?
            if not self._uppercase:
                token = token.lower()
            # end if

            if last_token2 is None:
                last_token2 = token
            if last_token1 is None:
                last_token1 = token
            else:
                # Bigram
                bigram = last_token2 + u" " + last_token1 + u" " + token

                # Add
                try:
                    voc_count[bigram] += 1.0
                except KeyError:
                    voc_count[bigram] = 1.0
                # end try

                # Preceding tokens
                last_token2 = last_token1
                last_token1 = token
            # end if
        # end for

        return voc_count
    # end __call__

    #########################################
    # Private
    #########################################

# end BagOf3Grams
