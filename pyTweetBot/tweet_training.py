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
from bs4 import BeautifulSoup
import urllib
import pickle

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


# Train a classifier on a dataset
def tweet_training(dataset_file, model_file="", test=False, param='dp', type='stat'):
    """
    Train a classifier on a dataset.
    :param config: pyTweetBot configuration object
    :param dataset_file: Path to the dataset file
    :param model_file: Path to model file if needed
    :param data: Title or content
    :param test: Test the classification success rate
    :param param: Model parameter (dp, ...)
    :param type: Model's type (stat, tfidf, stat2, textblob)
    """
    # Load model or create
    """if os.path.exists(model_file):
        model = StatisticalModel.load_from_file(model_file)
    else:
        if type == "stat":
            model = StatisticalModel("tweet_stat_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow(),
                                     smoothing=param, smoothing_param=0.5)
        elif type == "tfidf":
            model = TFIDFModel("tweet_tfidf_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow())
        elif type == "stat2":
            model = Statistical2GramModel("tweet_stat2_model", ['tweet', 'skip'],
                                          last_update=datetime.datetime.utcnow(), smoothing=param,
                                          smoothing_param=0.5)
        # end
    # end if"""

    # Load dataset
    """if os.path.exists(dataset_file):
        with open(dataset_file, 'r') as f:
            dataset = pickle.load(f)
            n_samples = len(dataset[0].keys())
        # end with
    else:
        logging.error(u"Cannot find dataset file {}".format(dataset_file))
    # end if

    # Train or test
    if not test:
        try:
            # For each URL in the dataset
            for index, url in enumerate(dataset[0].keys()):
                if not model.is_example_seen(url):
                    # Class
                    c = dataset[0][url]

                    # Log
                    print(u"Downloading example {}".format(url))

                    # Get URL's text
                    try:
                        html = urllib.urlopen(url).read().decode('utf-8', errors='ignore')
                        soup = BeautifulSoup(html, "lxml")
                        text = soup.get_text()

                        # HTML entities
                        text = clean_html_text(text)

                        # Train
                        logger.info(u"Training example {}/{} as {}...".format(index + 1, n_samples, c))
                        if ".fr" in url or ".ch" in url:
                            model.train(text, c)
                        else:
                            model.train(text, c)
                        # end if

                        # I've seen that
                        model.add_url(url)

                        # Display info
                        print(model)
                    except IOError as e:
                        logger.error(u"Error downloading example {} : {}".format(url, e))
                        model.add_url(url)
                        pass
                    except UnicodeError as e:
                        logger.error(u"URL contains unicode characters {}".format(url, e))
                        model.add_url(url)
                        pass
                    # end except
                # end if
            # end for
        except (KeyboardInterrupt, SystemExit):
            pass
        # end try

        # Save the model
        logger.info(u"Saving model to {}".format(args.model))
        model.save(args.model)
    else:
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
    # end if"""

# end tweet_training
