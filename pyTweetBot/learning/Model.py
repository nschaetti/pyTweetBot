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
import pickle
import md5


# Model not found exception
class ModelNotFoundException(Exception):
    """
    Model is not found.
    """
    pass
# end ModelNotFoundException


# Model already exists exception
class ModelAlreadyExistsException(Exception):
    """
    Model already exists.
    """
    pass
# end ModelAlreadyExistsException


# Learning model abstract class
class Model(object):
    """
    Learning model abstract class
    """

    # Variables
    _finalized = False

    # Constructor
    def __init__(self, features, name, classes):
        """
        Constructor
        """
        # Properties
        self._name = name
        self._classes = classes
        self._n_classes = len(classes)

        # Texts trained
        self._samples = list()

        # Features
        self._features = features
    # end __init__

    #################################################
    # Public
    #################################################

    # Train the model
    def update(self, x, y):
        """
        Train the model
        :param x: Training text
        :param y: Text's class
        """
        if not self.is_sample_seen(x):
            # Call training method
            self._train(self._features(x), y)

            # Add to memory
            self.add_sample(x)
        # end if
    # end train

    # Save the model
    def save(self, filename):
        """
        Save the model to a Pickle file
        :param filename:
        :return:
        """
        with open(filename, 'w') as f:
            pickle.dump(self, f)
        # end with
    # end save

    # Is trained on that example
    def is_sample_seen(self, x):
        """
        Is example already seen
        :param x: Training text
        :return:
        """
        if md5.new(u' '.join(x)).digest() in self._samples:
            return True
        else:
            return False
        # end if
    # end is_example_seen

    # Add to sample list
    def add_sample(self, x):
        """
        Add to text list
        :param x:
        """
        self._samples.append(md5.new(u' '.join(x)).digest())
    # end add_url

    #################################################
    # Override
    #################################################

    # Call the model
    def __call__(self, x):
        """
        Call the model to classify new text
        :param x: Text to classify
        :return: Resulting class number
        """
        return self._predict(self._features(x))
    # end __call__

    #################################################
    # Private
    #################################################

    # Predict
    def _predict(self, x):
        """
        Predict
        :param x: Text to classify
        :return:
        """
        pass
    # end _predict

    # Train an example
    def _train(self, x, y):
        """
        Train on a sample
        :param x: The text sample
        :param y: The class to predict
        :return:
        """
        pass
    # end _train

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
