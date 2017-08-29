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
        self._add_sample(title, url, u"pos")
    # end add_pos

    # Add a negative sample
    def add_neg(self, title, url):
        """
        Add a positive sample
        :param title:
        :param url:
        :return:
        """
        self._add_sample(title, url, u"neg")
    # end add_pos

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
