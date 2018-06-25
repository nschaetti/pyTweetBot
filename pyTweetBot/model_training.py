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
import sys
from learning.Model import Model
from learning.Dataset import Dataset
import tools.strings as pystr
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import pickle

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Train a classifier on a dataset
def model_training(data_set_file, model_file="", model_type='NaiveBayes'):
    """
    Train a classifier on a dataset.
    :param data_set_file: Path to the dataset file
    :param model_file: Path to model file if needed
    :param model_type: Model's type (stat, tfidf, stat2, textblob)
    """
    # Load model or create
    if os.path.exists(model_file):
        model = Model.load(model_file)
    else:
        if model_type == "NaiveBayes":
            model = MultinomialNB()
        elif model_type == "DecisionTree":
            model = DecisionTreeClassifier()
        elif model_type == "RandomForest":
            model = RandomForestClassifier()
        elif model_type == "SVM":
            model = svm.SVC()
        # end if
    # end if

    # Load dataset
    if os.path.exists(data_set_file):
        dataset = Dataset.load(data_set_file)
    else:
        sys.stderr.write(u"Cannot find dataset file {}\n".format(data_set_file))
        exit()
    # end if

    # Data and targets
    data = dataset.data
    targets = dataset.targets
    print(model)
    # Count, TFIDF, model
    text_clf = Pipeline([('vec', CountVectorizer(ngram_range=(1, 1))),
                         ('tfidf', TfidfTransformer()),
                         ('clf', model)])

    # Finalize training
    logging.getLogger(pystr.LOGGER).info(pystr.INFO_FINIALIZING_TRAINING)
    text_clf.fit(data, targets)

    # Show performance
    logging.getLogger(pystr.LOGGER).info(pystr.INFO_SAVING_MODEL.format(model_file))
    pickle.dump(text_clf, open(model_file, 'wb'))
# end if
