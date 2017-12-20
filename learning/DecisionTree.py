#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : DecisionTree.py
# Description : Decision Tree classifier class
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
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from .Classifier import Classifier


# Decision tree classifier
class DecisionTree(Classifier):
    """
    Decision tree
    """

    # Text classifier
    _training_finalized = False

    # Constructor
    def __init__(self, classes):
        """
        Constructor
        :param classes: Classes
        :param lang: Spacy language
        """
        super(DecisionTree, self).__init__(classes)
        # Properties
        self._token2index = dict()
        self._voc_size = 0
        self._samples = list()
        self._n_samples = 0
        self._tree_classifier = DecisionTreeClassifier(random_state=0)
    # end __init__

    ##############################################
    # Public
    ##############################################

    ##############################################
    # Override
    ##############################################

    # To str
    def __str__(self):
        """
        To string
        :return:
        """
        return "DecisionTree(classes={})".format(self._classes)
    # end __str__

    # To str
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"DecisionTree(classes={})".format(self._classes)
    # end __unicode__

    ##############################################
    # Private
    ##############################################

    # Train the model
    def _train(self, x, c, verbose=False):
        """
        Train
        :param x: Example's inputs
        :param c: Example's outputs
        :param verbose: Verbosity
        """
        # Add to voc
        for token in x.keys():
            try:
                test = self._token2index[token]
            except KeyError:
                self._token2index[token] = self._voc_size
                self._voc_size += 1
            # end try
        # end for

        # Add
        self._samples.append((x, c))
        self._n_samples += 1
    # end _train

    # Classify a document
    def _classify(self, x):
        """
        Classify a document.
        :param x: Document's text.
        :return: A tuple with found class and values per classes.
        """
        # Feature vector
        feature_vector = np.zeros(self._voc_size)

        # For each tokens
        for token in x.keys():
            try:
                feature_vector[self._token2index[token]] = x[token]
            except KeyError:
                pass
            # end try
        # end for

        # Predict
        y = self._tree_classifier.predict(list(x))
        y_prob = self._tree_classifier.predict_proba(list(x))

        return y[0], y_prob[0]
    # end _classify

    # Finalize the training
    def _finalize_training(self, verbose=False):
        """
        Finalize training.
        :param verbose: Verbosity
        """
        # List of feature vectors and labels
        vector_list = list()
        label_list = list()

        # For each sample
        for sample in self._samples:
            # Feature vector
            feature_vector = np.zeros(self._voc_size)

            # For each tokens
            for token in sample[0].keys():
                feature_vector[self._token2index[token]] = sample[0][token]
            # end for

            # Add
            vector_list.append(feature_vector)
            label_list.append(sample[1])
        # end for

        # Train
        self._tree_classifier.fit(vector_list, label_list)
    # end _finalize_training

    # Reset the model
    def _reset_model(self):
        """
        Reset the model
        """
        self._tree_classifier = DecisionTreeClassifier(self._classes)
    # end _reset_model

# end Classifier
