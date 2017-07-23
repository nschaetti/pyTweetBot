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
import argparse
import logging
import os
import datetime
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from learning.StatisticalModel import StatisticalModel
from learning.TFIDFModel import TFIDFModel
from bs4 import BeautifulSoup
import urllib
import pickle
from HTMLParser import HTMLParser

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

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--model", type=str, help="Model file", required=True)
    parser.add_argument("--test", action='store_true', default=False)
    parser.add_argument("--dataset", type=str, help="Dataset file", required=True)
    parser.add_argument("--param", type=str, help="Model parameter (if creation)", default='dp')
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--type", type=str, help="Model type (stat, tfidf)", default='stat')
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load configuration file
    config = BotConfig.load(args.config)

    # Connection to MySQL
    dbc = config.get_database_config()
    mysql_connector = DBConnector(host=dbc["host"], username=dbc["username"], password=dbc["password"],
                                  db_name=dbc["database"])

    # Load model or create
    if os.path.exists(args.model):
        model = StatisticalModel.load_from_file(args.model)
    else:
        if args.type == "stat":
            model = StatisticalModel("tweet_stat_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow(),
                                     smoothing=args.param, smoothing_param=0.5)
        else:
            model = TFIDFModel("tweet_tfidf_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow())
        # end
    # end if

    # Load dataset
    if os.path.exists(args.dataset):
        with open(args.dataset, 'r') as f:
            dataset = pickle.load(f)
            n_samples = len(dataset[0].keys())
        # end with
    else:
        logging.error(u"Cannot find dataset file {}".format(args.dataset))
    # end if

    # Train or test
    if not args.test:
        try:
            # For each URL in the dataset
            for index, url in enumerate(dataset[0].keys()):
                if not model.is_example_seen(url):
                    # Class
                    c = dataset[0][url]

                    # Log
                    logger.info(u"Downloading example {}".format(url))

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
    # end if

# end if
