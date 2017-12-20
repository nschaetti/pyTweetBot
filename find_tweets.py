#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : find_tweet.py
# Description : Find new tweets from various sources
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
import subprocess, signal
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from tweet.TweetFinder import TweetFinder
from tools.PageParser import PageParser, PageParserRetrievalError
import learning
import tweet as tw
import tools.strings as pystr

####################################################
# Globals
####################################################


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Find new tweets from various sources
def find_tweets(config, model, action_scheduler, n_pages=2, threshold=0.5):
    """
    Find tweet in the hunters
    :param config: BotConfig configuration object
    :param model: Path to model file for classification
    :param action_scheduler: Scheduler object
    :param n_pages: Number of pages to analyze
    :param threshold: Probability threshold to be accepted as tweet
    """
    p = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        try:
            print(line.encode('ascii', errors='ignore'))
        except UnicodeEncodeError:
            pass
        # end try
        #print(u"Process : {}".format(line.encode('ascii', errors='ignore')))
        """if 'pyTweetBot' in line:
            print(line)
        # end if"""
    # end for

    # Tweet finder
    tweet_finder = TweetFinder(shuffle=True)

    # Load model
    tokenizer, bow, model, censor = learning.Classifier.load_model(config, model)

    # Add RSS streams
    for rss_stream in config.rss:
        #tweet_finder.add(RSSHunter(rss_stream))
        pass
    # end for

    # Add Google News
    for news in config.google_news:
        # Add for each tuple language/country
        """for language in news['languages']:
            for country in news['countries']:
                tweet_finder.add(GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country,
                                                  hashtags=news['hashtags'], n_pages=n_pages))
            # end for
        # end for"""

        # Add as a Twitter hunter
        tweet_finder.add(tw.TwitterHunter(search_term=news['keyword'], hashtags=news['hashtags'], n_pages=n_pages,
                                          languages=news['languages']))
    # end for

    # For each tweet
    for tweet in tweet_finder:
        # On title
        on_title = False

        # Get page's text
        try:
            page_info = PageParser(tweet.get_url())
            page_text = page_info.text
        except PageParserRetrievalError as e:
            logging.getLogger(pystr.LOGGER).warning(pystr.WARNING_PAGE_RETRIEVAL.format(e))
            page_text = tweet.get_text()
            on_title = True
        # end try

        # Predict class
        prediction, probs = model(bow(tokenizer(page_text)))
        censor_prediction, _ = censor(page_text)

        # Predicted as tweet?
        if censor_prediction == "pos" and (prediction == "pos" or on_title) and not tweet.already_tweeted():
            if probs['pos'] >= threshold or on_title:
                if not on_title or probs['pos'] >= 0.9:
                    # Try to add
                    try:
                        logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_TWEET_SCHEDULER.format(
                            tweet.get_tweet()))
                        action_scheduler.add_tweet(tweet)
                    except ActionReservoirFullError:
                        logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL)
                        exit()
                        pass
                    except ActionAlreadyExists:
                        logging.getLogger(pystr.LOGGER).error(pystr.ERROR_TWEET_ALREADY_DB.format(
                            tweet.get_tweet().encode('ascii', errors='ignore')))
                        pass
                    # end try
                # end if
            # end if
        # end if
    # end for
# end if
