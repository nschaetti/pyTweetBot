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
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from retweet.RetweetFinder import RetweetFinder
from twitter.TweetBotConnect import TweetBotConnector
import pickle
from learning.Dataset import Dataset
import time

####################################################
# Main function
####################################################


# Get retweet data
def retweet_dataset(dataset_file, search, info=False):
    """
    Get retweet data
    :param config:
    :param dataset_file:
    :param n_pages:
    :param search: Search term
    :param info:
    :return:
    """
    # Load or create dataset
    if os.path.exists(dataset_file):
        print(u"Opening dataset file {}".format(dataset_file))
        dataset = Dataset.load(dataset_file)
    else:
        dataset = Dataset()
    # end if

    # Show informations
    if info:
        print(dataset)
        exit()
    # end if

    # Retweet finder
    retweet_finder = RetweetFinder(search_keywords=search, languages=['en', 'fr'])

    # For each tweet
    for tweet, polarity, subjectivity in retweet_finder:
        if not dataset.is_in(tweet.text):
            # Ask
            print(u"Would you classify the following element as negative(n) or positive(p)?")
            print(tweet.text)
            print(u"Polarity : {}".format(polarity))
            print(u"Subjectivity : {}".format(subjectivity))
            observed = raw_input(u"Positive or negative (p/n) (q for quit, s for skip) : ").lower()

            # Add as example
            if observed == 'q':
                break
            elif observed == 'p':
                dataset.add_positive(tweet.text)
            elif observed == 's':
                pass
            else:
                dataset.add_negative(tweet.text)
            # end if

            # Save dataset
            dataset.save(dataset_file)
        else:
            logging.debug(u"Already in stock : {}".format(tweet.text))
        # end if
    # end if

# end if
