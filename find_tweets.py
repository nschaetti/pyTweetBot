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
import signal
import os
import time
import sys
import nsNLP
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from tweet.TweetFactory import TweetFactory
from learning.CensorModel import CensorModel
from news.PageParser import PageParser, PageParserRetrievalError
from learning.tools import load_model
import learning
import tweet

####################################################
# Globals
####################################################

# Continue main loop?
cont_loop = True

####################################################
# Functions
####################################################


# Signal handler
def signal_handler(signum, frame):
    """
    Signal handler
    :param signum: Signal number to handle
    :param frame: Frame
    """
    global cont_loop
    logging.info(u"Signal {} received in frame {}".format(signum, frame))
    logging.info(u"Stopping loop at next iteration")
    cont_loop = False
# end signal_handler


####################################################
# Main function
####################################################

def find_tweets(config, model, action_scheduler, features, n_pages=2, threshold=0.5):
    """
    Find tweet in the hunters
    :param config: BotConfig configuration object
    :param model: Path to model file for classification
    :param action_scheduler: Scheduler object
    :param features: Features (words, bigrams, trigrams) separated by +
    :param n_pages: Number of pages to analyze
    :param threshold: Probability threshold to be accepted as tweet
    """

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Tweet finder
    tweet_finder = TweetFinder(shuffle=True)

    # Load model
    tokenizer, bow, model, censor = learning.Classifier().load_model(config, model, features)

    # Add RSS streams
    for rss_stream in config.rss:
        tweet_finder.add(RSSHunter(rss_stream))
    # end for

    # Add Google News
    for news in config.google_news:
        # Add for each tuple language/country
        for language in news['languages']:
            for country in news['countries']:
                tweet_finder.add(GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country,
                                                  hashtags=news['hashtags'], n_pages=n_pages))
            # end for
        # end for

        # Add as a Twitter hunter
        tweet_finder.add(tweet.TwitterHunter(search_term=news['keyword'], hashtags=news['hashtags'], n_pages=n_pages))
    # end for

    # Keep running
    while cont_loop:
        # For each tweet
        for tweet in tweet_finder:
            # Get page's text
            try:
                page_text = PageParser.get_text(tweet.get_url())
            except PageParserRetrievalError as e:
                logging.getLogger(u"pyTweetBot").error(u"Page retrieval error : {}".format(e))
                continue
            # end try

            # Predict class
            prediction, probs = model(bow(tokenizer(page_text)))
            censor_prediction, _ = censor(page_text)

            # Predicted as tweet
            if prediction == "pos" and censor_prediction == "pos" and not tweet.already_tweeted():
                if probs['pos'] >= threshold:
                    # Try to add
                    try:
                        logging.getLogger(u"pyTweetBot").info(u"Adding Tweet \"{}\" to the scheduler".format(
                            tweet.get_tweet()))
                        action_scheduler.add_tweet(tweet)
                    except ActionReservoirFullError:
                        logging.getLogger(u"pyTweetBot").error(u"Reservoir full for Tweet action, exiting...")
                        exit()
                        pass
                    except ActionAlreadyExists:
                        logging.getLogger(u"pyTweetBot").error(u"Tweet \"{}\" already exists in the database".format(
                            tweet.get_tweet().encode('ascii', errors='ignore')))
                        pass
                    # end try
                # end if
            # end if
        # end for
    # end while

# end if
