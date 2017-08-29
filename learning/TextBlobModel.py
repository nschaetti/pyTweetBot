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
from TextBlob.classifiers import NaiveBayesClassifier


# TextBlob naive bayes classifier
class TextBlobModel(object):
    """
    TextBlob naive bayes classifier
    """

    # Variables
    _finalized = False

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        super(TextBlobModel, self).__init__()

        # Classifier
        self._cl = NaiveBayesClassifier(train_set=[])
    # end __init__

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
        # Update the classifier
        self._cl.update((text, c))
    # end train

    #################################################
    # Private
    #################################################

    # Predict
    def _predict(self, text):
        """
        Predict
        :param text: Text to classify
        :return:
        """
        return self._cl.classify(text)
    # end _predict

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

    # Create a new model
    @staticmethod
    def create(opt, n_classes=None):
        """
        Create a new model in DB or file
        :param opt: Model options
        :param n_classes: Classes count if classification model.
        :return: The newly created model
        """
        return TextBlobModel()
    # end create

# end Model
