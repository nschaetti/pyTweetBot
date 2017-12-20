#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : model_testing.py
# Description : Function to test a model on a given dataset.
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
import learning
from learning.Dataset import Dataset


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Test a classifier
def model_testing(config, data_set_file, model_file, text_size=2000, threshold=0.5):
    """
    Test a classifier
    :param data_set_file: Path to the dataset file
    :param model_file: Path to model file if needed
    :param text_size: Minimum text size
    :param threshold: Probability threshold
    """
    # Load data set
    if os.path.exists(data_set_file):
        dataset = Dataset.load(data_set_file)
    else:
        logging.error(u"Cannot find data set file {}".format(data_set_file))
    # end if

    # Load model
    tokenizer, bow, model, censor = learning.Classifier.load_model(config, model_file)

    # Stats
    confusion_matrix = {'pos': {'pos': 0.0, 'neg': 0.0}, 'neg': {'pos': 0.0, 'neg': 0.0}}

    # Print model
    print(u"Using model {}".format(model))

    # For each URL in the dataset
    index = 1
    for text, c in dataset:
        if len(text) > text_size:
            # Log
            print(u"Testing sample {}".format(index))

            # Predict
            _, probs = model(bow(tokenizer.tokenize(text)))

            # Threshold
            if probs['pos'] > threshold:
                prediction = 'pos'
            else:
                prediction = 'neg'
            # end if

            # Save result
            confusion_matrix[prediction][c] += 1.0

            # Compare
            print(u"Predicted {} ({}) for observation {}".format(prediction, probs[prediction], c))

            # Print false positive
            if prediction == 'pos' and c == 'neg':
                print(u"")
                print(text)
                print(u"")
            # end if

            # Index
            index += 1
        # end if
    # end for

    # False positive/negative
    false_positive = confusion_matrix['pos']['neg'] / float(index-1)
    false_negative = confusion_matrix['neg']['pos'] / float(index-1)
    success_rate = (confusion_matrix['pos']['pos'] + confusion_matrix['neg']['neg']) / float(index-1)

    # Show performance
    print\
    (
        u"Success rate of {} on dataset, {} false positive, {} false negative"
            .format(success_rate*100.0, false_positive*100.0, false_negative*100.0)
    )

# end if
