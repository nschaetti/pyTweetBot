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
    def __init__(self, name, classes, last_update):
        # Superclass
        super(TFIDFModel, self).__init__()

        # Properties
        self._name = name
        self._classes = classes
        self._n_classes = len(classes)
        self._n_tokens = 0.0
        self._n_total_tokens = 0.0
        self._classes_counts = dict()
        self._classes_token_count = dict()
        self._collection_counts = dict()
        self._classes_vectors = dict()
        self._classes_frequency = dict()
        self._token_position = dict()
        self._last_update = last_update
        self._finalized = False

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
    def train(self, text, c, lang='en'):
        """
        Train the model
        :param text: Training text
        :param c: Text's class
        :param lang: Text's language
        """
        # Tokens
        tokens = spacy.load(lang)(text)

        # For each token
        for token in tokens:
            token_text = token.text.lower().replace(u" ", u"").replace(u"\t", u"")
            if len(token_text) > 1 and len(token_text) < 25 and self._filter_token(token_text):
                # Classes counts
                try:
                    self._classes_counts[c][token_text] += 1.0
                except KeyError:
                    self._classes_counts[c][token_text] = 1.0
                    self._n_tokens += 1.0
                # end try

                # Collection counts
                try:
                    self._collection_counts[token_text] += 1.0
                except KeyError:
                    self._collection_counts[token_text] = 1.0
                # end try

                # Classes token count
                try:
                    self._classes_token_count[c] += 1.0
                except KeyError:
                    self._classes_token_count[c] = 1.0
                # end try

                # Total tokens
                self._n_total_tokens += 1.0
            # end if
        # end token
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
        return "TFIDFModel(name={}, n_classes={}, last_training={}, " \
               "n_tokens={}, mem_size={}o)".format(self._name, self._n_classes,
                                                   self._last_update, self._n_tokens,
                                                   getsizeof(self))
    # end __str__

    ###############################################
    # Private
    ###############################################

    # Prediction
    def _predict(self, text, lang='en'):
        """
        Prediction
        :param text: Text to classify
        :return: Resulting class number
        """
        # Finalize
        if not self._finalized:
            self._finalize()
            self._finalized = True
        # end if

        # Tokens
        tokens = spacy.load(lang)(text)

        d_vector = np.zeros(len(self._collection_counts.keys()), dtype='float64')
        for token in tokens:
            token_text = token.text.lower().replace(u" ", u"").replace(u"\t", u"")
            if len(token_text) > 1 and len(token_text) < 25 and self._filter_token(token_text):
                try:
                    index = self._token_position[token_text]
                    d_vector[index] += 1.0
                except KeyError:
                    pass
                # end try
            # end if
        # end for

        # Normalize vector
        d_vector /= float(len(tokens))

        # For each classes
        similarity = np.zeros(len(self._classes_counts.keys()))
        for index, c in enumerate(self._classes_counts.keys()):
            similarity[index] = TFIDFModel.cosinus_similarity(self._classes_vectors[c], d_vector)
        # end for

        return self._classes_counts.keys()[np.argmax(similarity)]
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
                if self._classes_counts[c][token] > 0:
                    count += 1.0
                # end if
            # end for
            self._classes_frequency[token] = count
            # end for
        # end if

        # For each classes
        for c in self._classes_counts.keys():
            c_vector = np.zeros(len(self._classes_counts[c].keys()), dtype='float64')
            for token in self._collection_counts.keys():
                index = self._token_position[token]
                c_vector[index] = self._classes_counts[c][token]
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

    # Filter tokens
    def _filter_token(self, token):
        for sym in self._token_filter:
            if sym in token:
                return False
            # end if
        # end for
        return True
    # end _filter_token

    ####################################################
    # Static
    ####################################################

    # Load the model
    @staticmethod
    def load(filename):
        """
        Load the model from DB or file
        :param opt: Loading option
        :return: The model class
        """
        with open(filename, 'r') as f:
            return pickle.load(f)
        # end with
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
