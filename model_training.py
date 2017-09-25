#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
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

# Import
import logging
import os
import datetime
import sys
import nsNLP
from learning.Model import Model
from learning.StatisticalModel import StatisticalModel
from learning.Statistical2GramModel import Statistical2GramModel
from learning.TFIDFModel import TFIDFModel
from learning.TextBlobModel import TextBlobModel
from learning.Dataset import Dataset

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Train a classifier on a dataset
def model_training(data_set_file, model_file="", model_type='NaiveBayes', features='word'):
    """
    Train a classifier on a dataset.
    :param data_set_file: Path to the dataset file
    :param model_file: Path to model file if needed
    :param model_type: Model's type (stat, tfidf, stat2, textblob)
    :param features: Features
    """
    # Load model or create
    if os.path.exists(model_file):
        model = Model.load(model_file)
    else:
        if model_type == "stat":
            model = nsNLP.statistical_models.SLTextClassifier(
                classes=['pos', 'neg'],
                smoothing='dp',
                smoothing_param=0.05
            )
        elif model_type == "tfidf":
            model = nsNLP.statistical_models.TFIDFTextClassifier(
                classes=['pos', 'neg']
            )
        elif model_type == "NaiveBayes":
            model = nsNLP.statistical_models.NaiveBayesClassifier(
                classes=['pos', 'neg'],
                smoothing='dp',
                smoothing_param=0.05
            )
        # end if
    # end if

    # Tokenizer
    tokenizer = nsNLP.tokenization.NLTKTokenizer(lang='english')

    # Parse features
    feature_list = features.split('+')

    # Join features
    bow = nsNLP.features.BagOfGrams()

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
            sys.stderr.write(u"Unknown features type {}\n".format(bag))
            exit()
        # end if
        bow.add(b)
    # end for

    # Load dataset
    if os.path.exists(data_set_file):
        dataset = Dataset.load(data_set_file)
    else:
        sys.stderr.write(u"Cannot find dataset file {}\n".format(data_set_file))
        exit()
    # end if

    # Finalized?
    if not model.finalized():
        # For each text in the dataset
        index = 1
        for text, c in dataset:
            # Tokens
            tokens = tokenizer(text)

            # Log
            logging.getLogger(u"pyTweetBot").info\
            (
                u"Training model on example {}/{} with c={} and {} tokens".format(index, len(dataset), c, len(tokens))
            )

            # Add training example
            model.train(bow(tokens), c)

            # Info
            logging.getLogger(u"pyTweetBot").info\
            (
                u"Model with {} tokens (neg={}/pos={})".format(model.get_n_tokens(), model.get_n_tokens('neg'), model.get_n_tokens('pos'))
            )

            # Index
            index += 1
        # end for
    else:
        logging.getLogger(u"pyTweetBot").error(u"Model already finalized...")
        exit()
    # end if

    # Finalize training
    logging.getLogger(u"pyTweetBot").info(u"Finalizing training...")
    model.finalize()

    # Show performance
    logging.getLogger(u"pyTweetBot").info(u"Training finished... Saving model to {}".format(model_file))
    model.save(model_file)
# end if
