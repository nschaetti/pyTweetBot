#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Model.py
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
from db.obj.Model import Model as DbModel


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

    #################################################
    # Public
    #################################################

    # Train the model
    def train(self, text, c):
        """
        Train the model
        :param text: Training text
        :param c: Text's class
        """
        pass
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

    #################################################
    # Override
    #################################################

    # Call the model
    def __call__(self, text, lang='en'):
        """
        Call the model to classify new text
        :param text: Text to classify
        :return: Resulting class number
        """
        if not self._finalized:
            self._finalize()
            self._finalized = True
        # end if
        return self._predict(text, lang=lang)
    # end __call__

    #################################################
    # Private
    #################################################

    # Predict
    def _predict(self, text, lang='en'):
        """
        Predict
        :param text: Text to classify
        :return:
        """
        pass
    # end _predict

    # Finalize the model
    def _finalize(self):
        """
        Finalize the model
        :return:
        """
        pass
    # end _finalize

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
        pass
    # end load

    # Create a new model
    @staticmethod
    def create(opt, n_classes=None):
        """
        Create a new model in DB or file
        :param opt: Model options
        :param n_classes: Classes count if classification model.
        :return: The newly created model
        """
        pass
    # end create

    @staticmethod
    def exists(name):
        """
        Does a model exists?
        :param name: Model's name
        :return: True or False
        """
        return DbModel.exists(name)
    # end exists

# end Model
