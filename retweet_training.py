#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot train retweet classifier.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 30.07.2017 18:01:00
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
from learning.Model import Model
from learning.StatisticalModel import StatisticalModel
from learning.Statistical2GramModel import Statistical2GramModel
from learning.TFIDFModel import TFIDFModel
from bs4 import BeautifulSoup
import urllib
import pickle
from HTMLParser import HTMLParser

####################################################
# Functions
####################################################


####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Train retweet classifier")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--model", type=str, help="Model file", required=True)
    parser.add_argument("--test", action='store_true', default=False)
    parser.add_argument("--dataset", type=str, help="Dataset file", required=True)
    parser.add_argument("--param", type=str, help="Model parameter (if creation)", default='dp')
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--type", type=str, help="Model type (stat, tfidf, stat2)", default='stat')
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
        model = Model.load_from_file(args.model)
    else:
        if args.type == "stat":
            model = StatisticalModel("tweet_stat_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow(),
                                     smoothing=args.param, smoothing_param=0.5)
        elif args.type == "tfidf":
            model = TFIDFModel("tweet_tfidf_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow())
        elif args.type == "stat2":
            model = Statistical2GramModel("tweet_stat2_model", ['tweet', 'skip'],
                                          last_update=datetime.datetime.utcnow(), smoothing=args.param,
                                          smoothing_param=0.5)
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
            for index, tweet_text in enumerate(dataset[0].keys()):
                if not model.is_example_seen(tweet_text):
                    # Class
                    c = dataset[tweet_text]

                    # Log
                    logger.info(u"Tweet : {}".format(tweet_text))

                    # Train
                    logger.info(u"Training example {}/{} as {}...".format(index + 1, n_samples, c))
                    model.train(tweet_text, c)

                    # I've seen that
                    model.add_url(tweet_text)

                    # Display info
                    print(model)
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
        false_positive_texts = list()

        try:
            # For each URL in the dataset
            for tweet_text in dataset[0].keys():
                # Class
                c = dataset[tweet_text]

                # Log
                logger.info(u"Testing \"{}\"".format(tweet_text))

                # Predict
                prediction, probs = model(tweet_text)

                # Same result
                if probs['tweet'] == probs['skip']:
                    prediction = "skip"
                # end if

                # False positive
                if prediction == "tweet" and c == "skip":
                    false_positive += 1.0
                    false_positive_texts.append(tweet_text)
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
        for text in false_positive_texts:
            print(text)
        # end for
    # end if

# end if
