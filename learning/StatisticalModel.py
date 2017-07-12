#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : StatisticalMode.py
# Description : pyTweetBot statistical model for text classification.
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
from .Model import Model, ModelNotFoundException, ModelAlreadyExistsException
from db.obj.Model import Model as DbModel
from db.obj.ModelTokens import ModelToken
import spacy
import pickle
import decimal
from db.DBConnector import DBConnector


# A statistical model for text classification
class StatisticalModel(Model):
    """
    A statistical model for text classification
    """

    # Constructor
    def __init__(self, name, classes, tokens_probs, last_update, mu):
        """
        Constructor
        :param name: Model's name
        :param n_classes: Class count
        :param tokens_prob: Array of dictionaries of tokens probabilities
        """
        # Properties
        self._name = name
        self._classes = classes
        self._n_classes = len(classes)
        self._tokens_probs = tokens_probs
        self._last_update = last_update
        self._mu = mu

        # Init dicionaries
        self._token_counters = dict()
        self._class_counters = dict()
    # end __init__

    # Train the model
    def train(self, text, c):
        """
        Train the model
        :param text: Training text
        :param c: Text's class
        """
        # Tokens
        tokens = spacy.load('en')(text)

        # For each token
        for token in tokens:
            # Token counters
            if token.text in self._token_counters.keys():
                self._token_counters[token.text] += decimal.Decimal(1.0)
            else:
                self._token_counters[token.text] = decimal.Decimal(1.0)
            # end if

            # Create entry in class counter
            if token.text not in self._class_counters.keys():
                self._class_counters[token.text] = dict()
            # end if

            # Class counters
            if c in self._class_counters[token.text].keys():
                self._class_counters[token.text][c] += decimal.Decimal(1.0)
            else:
                self._class_counters[token.text][c] = decimal.Decimal(1.0)
            # end if
        # end token
    # end train

    # Call the model
    def __call__(self, text):
        """
        Call the model to classify new text
        :param text: Text to classify
        :return: Resulting class number
        """
        # Text's probabilities
        text_probs = list()

        # Init
        for c in range(self._n_classes):
            text_probs[c] = decimal.Decimal(1.0)
        # end for

        # Parse text
        text_tokens = spacy.load('en')(text)

        # Get all tokens
        tokens = list()
        for token in text_tokens:
            tokens.append(token)
        # end for

        # For each token
        for token in tokens:
            # Get token probs for each class
            token_probs = self[token.text]

            # For each class
            for c in self._classes:
                text_probs[c] *= decimal.Decimal(
                    StatisticalModel.smooth(token_probs[c], self._token_counters[token], len(tokens), mu=self._mu))
            # end for
        # end for

        # Get highest prob
        max = decimal.Decimal(0.0)
        result_class = ""
        for c in self._classes:
            if text_probs[c] > max:
                max = text_probs[c]
                result_class = c
            # end if
        # end for

        return result_class
    # end __call__

    # Get token probability
    def __getitem__(self, item):
        # Exists
        if item in self._class_counters:
            probs = self._class_counters[item]
        else:
            probs = dict()
        # end if

        # Set default
        for c in self._classes:
            if c not in probs:
                probs[c] = decimal.Decimal(0.0)
            else:
                probs[c] = probs[c] / self._token_counters[item]
            # end if
        # end for

        return probs
    # end __getitem__

    # To String
    def __str__(self):
        """
        To string
        :return:
        """
        return "StatisticalModel(name={}, n_classes={}, last_training={}".format(self._name, self._n_classes,
                                                                                 self._last_update)
    # end __str__

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

    # Load the model
    @staticmethod
    def load(opt):
        """
        Load the model from DB or file
        :param opt: Loading option
        :return: The model class
        """
        # Get from DB
        model = DbModel.get_by_name(opt)

        # Check if exists
        if model is not None:
            # Array with an entry for each class
            class_tokens = list()

            # For each classes
            for i in range(model.model_n_classes):
                class_tokens.append(ModelToken.get_tokens(model=model, c=i))
            # end for

            return StatisticalModel(model.model_name, model.model_n_classes, class_tokens)
        else:
            raise ModelNotFoundException(u"Statistical model {} not found in the database".format(opt))
        # end if
    # end load

    # Load the model from file
    @staticmethod
    def load_from_file(filename):
        """
        Load the model from a Pickle file
        :param filename: Pickle file
        :return: The loaded class
        """
        with open(filename, 'r') as f:
            return pickle.load(f)
        # end with
    # end load_from_file

    # create a new model
    @staticmethod
    def create(opt, n_classes=None):
        """
        create a new model in db or file
        :param opt: model options
        :param n_classes: Number of classes to classify.
        :return: the newly created model
        """
        # Check if model already exists
        if not DbModel.exists(opt):
            model = DbModel(model_name=opt, model_n_classes=n_classes)
            DBConnector().get_session().add(model)
            DBConnector().get_session().commit()
        else:
            raise ModelAlreadyExistsException("This model's name already exists in the database!")
        # end if

        return model
    # end create

        # Model exists?

    @staticmethod
    def exists(name):
        """
        Does a model exists?
        :param name: Model's name
        :return: True or False
        """
        return DbModel.exists(name)
    # end exists

    # Smooth function
    @staticmethod
    def smooth(doc_prob, col_prob, doc_length, mu):
        return (float(doc_length) / (float(doc_length) + float(mu))) * doc_prob + \
               (float(mu) / (float(mu) + float(doc_length))) * col_prob
    # end smooth

# end StatisticalModel
