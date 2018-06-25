#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : TextBlobModel.py
# Description : pyTweetBot learning model abstract céass
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
import pickle
import sys
import json
# import pyTweetBot.learning.features as features

sys.setrecursionlimit(10000)


# A dataset for training
class Dataset(object):
    """
    A dataset of URL and title for training
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        # Data
        self._texts = list()
        self._n_texts = 0
        self._n_positive_texts = 0
        self._n_negative_texts = 0
        self._pos = 0
    # end __init__

    #################################################
    # Properties
    #################################################

    # Data
    @property
    def data(self):
        """
        Data
        :return:
        """
        data = list()
        for (text, c) in self._texts:
            data.append(text)
        # end for
        return data
    # end data

    # Targets
    @property
    def targets(self):
        """
        Targets
        :return:
        """
        targets = list()
        for (text, c) in self._texts:
            """if c == 'neg':
                targets.append(0)
            else:
                targets.append(1)
            # end if"""
            targets.append(c)
        # end for
        return targets
    # end targets

    #################################################
    # Public
    #################################################

    # Get texts
    def get_texts(self):
        """
        Get texts
        :return:
        """
        return self._texts
    # end get_texts

    # Add a positive sample
    def add_positive(self, text):
        """
        Add a positive sample
        :param text:
        :return:
        """
        if self._add_sample(text, u"pos"):
            self._n_positive_texts += 1
            return True
        else:
            return False
        # end if
    # end add_pos

    # Add a negative sample
    def add_negative(self, text):
        """
        Add a positive sample
        :param text:
        :return:
        """
        if self._add_sample(text, u"neg"):
            self._n_negative_texts += 1
            return True
        else:
            return False
        # end if
    # end add_pos

    # Save the dataset
    def save(self, filename):
        """
        Save the dataset
        :param filename:
        """
        with open(filename, 'w') as f:
            pickle.dump(self, f)
        # end with
    # end save

    # Is in dataset
    def is_in(self, ttext):
        """
        Is in dataset?
        :param ttext:
        :return:
        """
        found = False
        for (text, c) in self._texts:
            if text == ttext:
                found = True
            # end if
        # end for
        return found
    # end is_in

    # To JSON
    def to_json(self):
        """
        To JSON
        :return:
        """
        # Samples
        samples = list()

        # For each text
        for text, c in self._texts:
            samples.append({'text': text, 'label': c})
        # end for

        # Return JSON
        return json.dumps(samples)
    # end to_json

    #################################################
    # Override
    #################################################

    # Length
    def __len__(self):
        """
        Length
        :return:
        """
        return self._n_texts
    # end __len__

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return:
        """
        return self
    # end __iter__

    # Next element
    def next(self):
        """
        Next element
        :return:
        """
        if self._pos >= len(self._texts):
            self._pos = 0
            raise StopIteration()
        else:
            self._pos += 1
            return self._texts[self._pos-1]
        # end if
    # end next

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        str = "Total number of samples in the dataset : {}\n".format(self._n_texts)
        str += "Number of positive samples : {}\n".format(self._n_positive_texts)
        str += "Number of negative samples : {}".format(self._n_negative_texts)
        return str
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To string
        :return:
        """
        str = u"Total number of samples in the dataset : {}\n".format(self._n_texts)
        str += u"Number of positive samples : {}\n".format(self._n_positive_texts)
        str += u"Number of negative samples : {}".format(self._n_negative_texts)
        return str
    # end __unicode__

    #################################################
    # Private
    #################################################

    # Add a sample
    def _add_sample(self, text, c):
        """
        Add a sample
        :param text:
        :param c:
        :return:
        """
        if (text, c) not in self._texts:
            self._texts.append((text, c))
            self._n_texts += 1
            return True
        else:
            return False
        # end if
    # end _add_sample

    #################################################
    # Static
    #################################################

    # Load the model
    @staticmethod
    def load(opt):
        """
        Load the model from DB or file
        :param opt: Loading option
        :return: The model class
        """
        return pickle.load(open(opt, 'rb'))
    # end load

# end Model
