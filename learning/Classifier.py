#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Classifier.py
# Description : Classifier base class
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
import nsNLP
import sys
from CensorModel import CensorModel


# Classifier base class
class Classifier(object):
    """
    Classifier
    """

    # Constructor
    def __init__(self, features, language='english'):
        """
        Constructor
        :param config: Settings
        """
        # Tokenizer
        self._tokenizer = nsNLP.tokenization.NLTKTokenizer(lang=language)

        # Parse features
        feature_list = features.split('+')

        # Join features
        self._bow = nsNLP.features.BagOfGrams()

        # For each features
        for bag in feature_list:
            # Select features
            if bag == 'words':
                b = nsNLP.features.BagOfWords()
            elif bag == 'bigrams':
                b = nsNLP.features.BagOf2Grams()
            elif bag == 'trigrams':
                b = nsNLP.features.BagOf3Grams()
            else:
                sys.stderr.write(u"Unknown features type {}".format(features))
                exit()
            # end if
            self._bow.add(b)
        # end for
    # end __init__

    #################################################
    # Public
    #################################################

    #################################################
    # Override
    #################################################

    # Predict
    def __call__(self, x):
        """
        Predict
        :param x: Text to classify
        :return:
        """
        pass
    # end __call__

    #################################################
    # Private
    #################################################

    # Predict
    def _predict(self, x):
        """
        Predict
        :param x:
        :return:
        """
        pass
    # end _predict

    #################################################
    # Static
    #################################################

    # Load a complete model and censor with path to model
    @staticmethod
    def load_model(config, model):
        """
        Load a complete model and censor with path to model
        :param config:
        :param model:
        :return:
        """
        # Load model
        model = nsNLP.classifiers.TextClassifier.load(model)
        censor = CensorModel(config)

        # Tokenizer
        tokenizer = nsNLP.tokenization.NLTKTokenizer(lang='english')

        # Join features
        bow = nsNLP.features.BagOfGrams()

        # Bag of gram, 2-grams, 3-grams
        bow.add(nsNLP.features.BagOfWords())
        bow.add(nsNLP.features.BagOf2Grams())
        bow.add(nsNLP.features.BagOf3Grams())

        return tokenizer, bow, model, censor
    # end load_model

# end Model

