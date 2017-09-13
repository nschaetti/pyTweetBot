#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Model.py
# Description : pyTweetBot learning model abstract class
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
import spacy


# Extract a bag of 2grams
class BagOf2Grams(object):
    """
    Extract a bag of words from text
    """

    # Constructor
    def __init__(self, lang='en', filters=None, uppercase=False):
        """
        Constructor
        """
        # Properties
        self._lang = lang
        self._nlp = spacy.load(lang)
        self._filters = filters
        self._uppercase = uppercase
    # end __init__

    ########################################
    # Override
    ########################################

    # Compute a text
    def __call__(self, text):
        """
        Compute a text
        :param text:
        :return:
        """
        # Result
        result = list()

        # Filter each token
        if self._filters is not None:
            for token in self._nlp(text):
                found = False
                for c in self._filters:
                    if c in token:
                        found = True
                    # end if
                # end for
                if not found:
                    result.append(token)
                # end if
            # end for
            return result
        else:
            return self._nlp(text)
        # end if
    # end __call__

# end BagOfWords
