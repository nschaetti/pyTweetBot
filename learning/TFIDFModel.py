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
import spacy
from .Model import Model, ModelNotFoundException, ModelAlreadyExistsException
from db.obj.Model import Model as DbModel
import decimal
import math
from numpy import linalg as LA
import numpy as np
import pickle
from sys import getsizeof


# A TFIDF model
class TFIDFModel(Model):
    """
    A TFIDF model
    """

    # Constructor
    def __init__(self, features, name, classes):
        """
        Constructor
        :param name:
        :param classes:
        :param last_update:
        """
        # Superclass
        super(TFIDFModel, self).__init__(features=features, name=name, classes=classes)

        # Properties
        self._n_tokens = 0.0
        self._n_total_tokens = 0.0
        self._classes_counts = dict()
        self._classes_token_count = dict()
        self._collection_counts = dict()
        self._classes_vectors = dict()
        self._classes_frequency = dict()
        self._token_position = dict()

        # Class counters init
        for c in classes:
            self._classes_counts[c] = dict()
            self._classes_token_count[c] = 0.0
        # end for

        # Regex
        self._token_filter = u"+\"*ç%&/()=?§°!£.,±“#Ç[]|{}≠¿¢«…Ç∞”‹⁄[]\ÒÔÚÿÆ•÷»<>≤≥\\_;:\n\r@∑€®†Ω°¡øπ¬∆ºª@ƒ∂ßå¥≈©√∫~'"
    # end __init__

    ####################################################
    # Public
    ####################################################

    # Train the model
    def train(self, x, y):
        """
        Train the model
        :param x: Training text
        :param y: Text's class
        """
        # For each token
        for token in x:
            # Classes counts
            try:
                self._classes_counts[y][token] += 1.0
            except KeyError:
                self._classes_counts[y][token] = 1.0
            # end try

            # Collection counts
            try:
                self._collection_counts[token] += 1.0
            except KeyError:
                self._collection_counts[token] = 1.0
                self._n_tokens += 1
            # end try

            # Classes token count
            try:
                self._classes_token_count[y] += 1.0
            except KeyError:
                self._classes_token_count[y] = 1.0
            # end try

            # Total tokens
            self._n_total_tokens += 1.0
        # end for
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

    ####################################################
    # Override
    ####################################################

    # To String
    def __str__(self):
        """
        To string
        :return:
        """
        return "TFIDFModel(name={}, n_classes={}, " \
               "n_tokens={}, mem_size={}o)".format(self._name, self._n_classes, self._n_tokens, getsizeof(self))
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"TFIDFModel(name={}, n_classes={}, " \
               u"n_tokens={}, mem_size={}o)".format(self._name, self._n_classes, self._n_tokens, getsizeof(self))
    # end __str__

    ###############################################
    # Private
    ###############################################

    # Prediction
    def _predict(self, x):
        """
        Prediction
        :param x: Text to classify
        :return: Resulting class number
        """
        # Finalize
        if not self._finalized:
            self._finalize()
            self._finalized = True
        # end if

        # Compute document vector
        d_vector = np.zeros(len(self._collection_counts.keys()), dtype='float64')
        for token in x:
            try:
                index = self._token_position[token]
                d_vector[index] += 1.0
            except KeyError:
                pass
            # end try
        # end for

        # Normalize vector
        d_vector /= float(len(x))

        # Compute classes vectors
        similarity = dict()
        for index, c in enumerate(self._classes_counts.keys()):
            similarity[c] = TFIDFModel.cosinus_similarity(self._classes_vectors[c], d_vector)
        # end for

        # Get highest prob
        max = 0.0
        result_class = ""
        for c in self._classes:
            if similarity[c] > max:
                max = similarity[c]
                result_class = c
            # end if
        # end for

        return result_class, similarity
    # end _predict

    # Finalize
    def _finalize(self):
        """
        Finalize
        :return:
        """
        # Position of each token
        i = 0
        for token in sorted(self._collection_counts.keys()):
            self._token_position[token] = i
            i += 1
        # end for

        # Compute classes frequency
        for token in self._collection_counts.keys():
            count = 0.0
            for c in self._classes_counts.keys():
                try:
                    if self._classes_counts[c][token] > 0:
                        count += 1.0
                    # end if
                except KeyError:
                    pass
                # end try
            # end for
            self._classes_frequency[token] = count
            # end for
        # end if

        # For each classes
        for c in self._classes_counts.keys():
            c_vector = np.zeros(len(self._collection_counts.keys()), dtype='float64')
            for token in self._collection_counts.keys():
                index = self._token_position[token]
                try:
                    c_vector[index] = self._classes_counts[c][token]
                except KeyError:
                    c_vector[index] = 0
                # end try
            # end for
            c_vector /= float(self._classes_token_count[c])
            for token in self._collection_counts.keys():
                index = self._token_position[token]
                if self._classes_frequency[token] > 0:
                    c_vector[index] *= math.log(self._n_classes / self._classes_frequency[token])
                # end if
            # end for
            self._classes_vectors[c] = c_vector
        # end for
    # end finalize

    ####################################################
    # Static
    ####################################################

    # Cosinus similarity
    @staticmethod
    def cosinus_similarity(a, b):
        """
        Cosinus similarity
        :param a:
        :param b:
        :return:
        """
        return np.dot(a, b) / (LA.norm(a) * LA.norm(b))
    # end cosinus_similarity

# end Model
