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
from sys import getsizeof
import re


# A statistical model for text classification
class StatisticalModel(Model):
    """
    A statistical model for text classification
    """

    # Constructor
    def __init__(self, name, classes, last_update, smoothing, smoothing_param):
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
        self._last_update = last_update
        self._n_token = 0
        self._n_total_token = 0

        # Init dicionaries
        self._token_counters = dict()
        self._class_counters = dict()

        # URL trained
        self._urls = list()

        # Smoothing
        self._smoothing = smoothing
        self._smoothing_param = smoothing_param

        # Regex
        self._token_filter = u"+\"*ç%&/()=?§°!£.,±“#Ç[]|{}≠¿¢«…Ç∞”‹⁄[]\ÒÔÚÿÆ•÷»<>≤≥\\_;:\n\r@∑€®†Ω°¡øπ¬∆ºª@ƒ∂ßå¥≈©√∫~'"
    # end __init__

    #####################################################
    # Public
    #####################################################

    # Get token count
    def get_token_count(self):
        """
        Get token count
        :return:
        """
        return len(self._token_counters.keys())
    # end get_token_count

    # Train the model
    def train(self, text, c, lang='en'):
        """
        Train the model
        :param text: Training text
        :param c: Text's class
        """
        # Tokens
        tokens = spacy.load(lang)(text)

        # For each token
        for token in tokens:
            token_text = token.text.lower().replace(u" ", u"").replace(u"\t", u"")
            if len(token_text) > 1 and len(token_text) < 25 and self._filter_token(token_text):
                #print token_text + u" ",
                # Token counters
                try:
                    self._token_counters[token_text] += 1.0
                except KeyError:
                    self._token_counters[token_text] = 1.0
                    self._n_token += 1.0
                # end try

                # Create entry in class counter
                try:
                    probs = self._class_counters[token_text]
                except KeyError:
                    self._class_counters[token_text] = dict()
                # end try

                # Class counters
                if c in self._class_counters[token_text].keys():
                    self._class_counters[token_text][c] += 1.0
                else:
                    self._class_counters[token_text][c] = 1.0
                # end if

                # One more token
                self._n_total_token += 1.0
            # end if
        # end token
    # end train

    # Add to url list
    def add_url(self, url):
        """
        Add to URL list
        :param url:
        :return:
        """
        self._urls.append(url)
    # end add_url

    # Is trained on that example
    def is_example_seen(self, url):
        """
        Is example already seen
        :param url:
        :return:
        """
        if url in self._urls:
            return True
        else:
            return False
        # end if
    # end is_example_seen

    ####################################################
    # Override
    ####################################################

    # Get token probability
    def __getitem__(self, item):
        """
        Get token probability
        :param item:
        :return:
        """
        # Probs
        probs = dict()

        # Set default
        for c in self._classes:
            try:
                probs[c] = self._class_counters[item][c] / self._token_counters[item]
            except KeyError:
                probs[c] = 0.0
            # end try
        # end for

        return probs
    # end __getitem__

    # To String
    def __str__(self):
        """
        To string
        :return:
        """
        return "StatisticalModel(name={}, n_classes={}, last_training={}, n_tokens={}, mem_size={}o, " \
               "token_counters_mem_size={} Go, class_counters_mem_size={} Go, n_total_token={})"\
            .format(self._name, self._n_classes,self._last_update, self.get_token_count(),
                    getsizeof(self), round(getsizeof(self._token_counters)/1073741824.0, 4),
                    round(getsizeof(self._class_counters)/1073741824.0, 4), self._n_total_token)
    # end __str__

    ####################################################
    # Private
    ####################################################

    # Prediction
    def _predict(self, text, lang='en'):
        """
        Prediction
        :param text: Text to classify
        :return: Resulting class number
        """
        # Text's probabilities
        text_probs = dict()

        # Init
        for c in self._classes:
            text_probs[c] = decimal.Decimal(1.0)
        # end for

        # Parse text
        text_tokens = spacy.load(lang)(text)

        # Get all tokens
        tokens = list()
        for token in text_tokens:
            tokens.append(token)
        # end for

        # For each token
        for token in tokens:
            token_text = token.text.lower()
            if len(token_text) > 1 and len(token_text) < 25 and self._filter_token(token_text):
                # Get token probs for each class
                try:
                    token_probs = self[token_text]
                    collection_prob = self._token_counters[token_text] / self._n_total_token
                except KeyError:
                    continue
                # end try
                #print(u"#" + token_text + u"#")
                #print(token_probs)
                #print(collection_prob)
                # For each class
                for c in self._classes:
                    smoothed_value = StatisticalModel.smooth(self._smoothing, token_probs[c], collection_prob, len(tokens),
                                                             param=self._smoothing_param)
                    #print(c + ":" + str(smoothed_value))
                    text_probs[c] *= decimal.Decimal(smoothed_value)
                # end for
            # end if
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

        return (result_class, text_probs)
    # end _predict

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

    # Dirichlet prior smoothing function
    @staticmethod
    def smooth_dirichlet_prior(doc_prob, col_prob, doc_length, mu):
        """
        Dirichlet prior smoothing function
        :param doc_prob:
        :param col_prob:
        :param doc_length:
        :param mu:
        :return:
        """
        return (float(doc_length) / (float(doc_length) + float(mu))) * doc_prob + \
               (float(mu) / (float(mu) + float(doc_length))) * col_prob
    # end smooth

    # Jelinek Mercer smoothing function
    @staticmethod
    def smooth_jelinek_mercer(doc_prob, col_prob, param_lambda):
        """
        Jelinek Mercer smoothing function
        :param col_prob:
        :param param_lambda:
        :return:
        """
        return (1.0 - param_lambda) * doc_prob + param_lambda * col_prob
    # end smooth

    # Smoothing function
    @staticmethod
    def smooth(smooth_algo, doc_prob, col_prob, doc_length, param):
        """
        Smoothing function
        :param smooth_algo: Algo type
        :param doc_prob:
        :param col_prob:
        :param doc_length:
        :param param:
        :return:
        """
        if smooth_algo == "dp":
            return StatisticalModel.smooth_dirichlet_prior(doc_prob, col_prob, doc_length, param)
        else:
            return StatisticalModel.smooth_jelinek_mercer(doc_prob, col_prob, param)
        # end if
    # end smooth

# end StatisticalModel
