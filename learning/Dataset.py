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
        self._urls = list()
        self._titles = list()
        self._samples = list()
        self._n_samples = 0
        self._n_positive_samples = 0
        self._n_negative_samples = 0
        self._pos = 0
    # end __init__

    #################################################
    # Public
    #################################################

    # Add a positive sample
    def add_pos(self, title, url):
        """
        Add a positive sample
        :param title:
        :param url:
        :return:
        """
        if self._add_sample(title, url, u"pos"):
            self._n_positive_samples += 1
            return True
        else:
            return False
        # end if
    # end add_pos

    # Add a negative sample
    def add_neg(self, title, url):
        """
        Add a positive sample
        :param title:
        :param url:
        :return:
        """
        if self._add_sample(title, url, u"neg"):
            self._n_negative_samples += 1
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
        pickle.dump(self, open(filename, 'w'))
    # end save

    # Is in dataset
    def is_in(self, title, url):
        """
        Is in dataset?
        :param title:
        :param url:
        :return:
        """
        return title in self._titles and url in self._urls
    # end is_in

    #################################################
    # Override
    #################################################

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
        if self._pos >= len(self._samples):
            raise StopIteration()
        else:
            self._pos += 1
            return self._samples[self._pos-1]
        # end if
    # end next

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        print(u"Total number of samples in the dataset : {}".format(self._n_samples))
        print(u"Number of positive samples : {}".format(self._n_positive_samples))
        print(u"Number of negative samples : {}".format(self._n_negative_samples))
    # end __str__

    #################################################
    # Private
    #################################################

    # Add a sample
    def _add_sample(self, title, url, c):
        """
        Add a sample
        :param title:
        :param url:
        :param c:
        :return:
        """
        if title not in self._titles and url not in self._urls:
            self._urls.append(url)
            self._titles.append(title)
            self._samples.append((title, url, c))
            self._n_samples += 1
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
        return pickle.load(open(opt, 'r'))
    # end load

# end Model
