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
from twitter.TweetBotConnect import TweetBotConnector
import pickle

####################################################
# Main function
####################################################


# Create a tweet dataset
def tweet_dataset(config, dataset_file, n_pages, info, rss):
    """
    Create a tweet dataset
    :param config:
    :param tweet_connector:
    :return:
    """
    # Load or create dataset
    if os.path.exists(dataset_file):
        with open(dataset_file, 'r') as f:
            (urls, texts) = pickle.load(f)
            # end with
    else:
        urls = dict()
        texts = list()
    # end if

    # Show informations
    if info:
        # Compute statistics
        examples_count = len(urls.keys())
        tweet_count = 0
        skip_count = 0
        for url in urls.keys():
            if urls[url] == "tweet":
                tweet_count += 1
            else:
                skip_count += 1
                # end if
        # end for

        # Print info
        print(u"{} examples in the dataset".format(examples_count))
        print(u"{} examples in the tweet class".format(tweet_count))
        print(u"{} examples in the skip class".format(skip_count))
        exit()
    # end if

    # Tweet finder
    tweet_finder = TweetFinder(shuffle=True)

    if rss == "":
        # Add RSS streams
        for rss_stream in config.get_rss_streams():
            tweet_finder.add(RSSHunter(rss_stream))
        # end for

        # Add Google News
        for news in config.get_news_config():
            for language in news['languages']:
                for country in news['countries']:
                    tweet_finder.add(
                        GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country, n_pages=n_pages))
                # end for
            # end for
        # end for
    else:
        tweet_finder.add(RSSHunter({'url': rss, 'hashtags': []}))
    # end if

    # For each tweet
    for tweet in tweet_finder:
        if tweet.get_url() not in urls.keys() and tweet.get_text() not in texts:
            # Ask
            print(tweet.get_text())
            print(tweet.get_url())
            observed = raw_input("Tweet or Skip (t/S/e)? ").lower()

            # Add as example
            if observed == "e":
                break
            elif observed == "t":
                urls[tweet.get_url()] = "tweet"
            else:
                urls[tweet.get_url()] = "skip"
            # end if

            # Add tweet
            texts.append(tweet.get_text())

            # Save dataset
            with open(dataset_file, 'w') as f:
                pickle.dump((urls, texts), f)
            # end with
        else:
            logging.debug(u"Already in stock : {}".format(tweet.get_url()))
        # end if
    # end for

# end if
