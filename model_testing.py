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
import urllib
from bs4 import BeautifulSoup
from learning.Model import Model
from learning.Dataset import Dataset


####################################################
# Functions
####################################################


# Clean HTML text
def clean_html_text(to_clean):
    """
    Clean HTML text
    :param to_clean:
    :return:
    """
    to_clean = to_clean.replace(u"%20", u" ")
    to_clean = to_clean.replace(u"%22", u"\"")
    to_clean = to_clean.replace(u"%3A", u":")
    to_clean = to_clean.replace(u"%2C", u",")
    to_clean = to_clean.replace(u"%2F", u"/")
    to_clean = to_clean.replace(u"%7B", u"{")
    to_clean = to_clean.replace(u"%7D", u"}")
    to_clean = to_clean.replace(u"%5B", u"[")
    to_clean = to_clean.replace(u"%5D", u"]")
    to_clean = to_clean.replace(u"%E2%80%99", u"'")
    to_clean = to_clean.strip()
    to_clean = to_clean.replace(u"\n", u"")
    to_clean = to_clean.replace(u"\r", u"")
    to_clean = to_clean.replace(u"\t", u"")
    return to_clean
# end clean_html_text

####################################################
# Main function
####################################################


# Test a classifier
def model_testing(data_set_file, model_file):
    """
    Test a classifier
    :param data_set_file: Path to the dataset file
    :param model_file: Path to model file if needed
    """
    # Load model or create
    if os.path.exists(model_file):
        model = Model.load(model_file)
    else:
        sys.stderr.write(u"Can't open model file {}\n".format(model_file))
        exit()
    # end if

    # Load data set
    if os.path.exists(data_set_file):
        dataset = Dataset.load(data_set_file)
    else:
        logging.error(u"Cannot find dataset file {}".format(data_set_file))
    # end if

    # Stats
    count = 0.0
    success = 0.0
    false_positive = 0.0
    false_positive_urls = list()

    try:
        # For each URL in the dataset
        for url in dataset[0].keys():
            # Class
            c = dataset[0][url]

            # Log
            logger.info(u"Testing {}".format(url))

            # Get URL's text
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")
            text = soup.get_text()

            # HTML entities
            text = clean_html_text(text)

            # Predict
            if ".fr" in url or ".ch" in url:
                prediction, probs = model(text)
            else:
                prediction, probs = model(text)
            # end if

            # Same result
            if probs['tweet'] == probs['skip']:
                prediction = "skip"
            # end if

            # False positive
            if prediction == "tweet" and c == "skip":
                false_positive += 1.0
                false_positive_urls.append(url)
            # end if

            # Compare
            logger.info(u"Predicted {} for observation {}".format(prediction, c))
            if prediction == c:
                success += 1.0
            # end if
            count += 1.0
        # end for
    except (KeyboardInterrupt, SystemExit):
        pass
    # end try

    # Show performance
    logger.info(u"Success rate of {} on dataset, {} false positive".format(success / count * 100.0,
                                                                           false_positive / count * 100.0))

    # Show false positives
    logger.info(u"False positives")
    for url in false_positive_urls:
        print(url)
    # end for

# end if
