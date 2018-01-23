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
import numpy as np
from learning.Dataset import Dataset
import pickle
import tools.strings as pystr


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Test a classifier
def model_testing(data_set_file, model_file, text_size=2000, threshold=0.5):
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

    # Data and targets
    pre_data = dataset.data
    pre_targets = dataset.targets

    # Data
    data = list()
    targets = list()
    for index, text in enumerate(pre_data):
        if len(text) >= text_size:
            data.append(text)
            targets.append(pre_targets[index])
        # end if
    # end for

    # Load model
    text_clf = pickle.load(open(model_file, 'rb'))

    # Predicted
    predicted = text_clf.predict(data)

    # Test
    success_rate = np.mean(predicted == targets)

    # Show performance
    print\
    (
        pystr.INFO_TEST_RESULT.format(success_rate*100.0)
    )
# end if
