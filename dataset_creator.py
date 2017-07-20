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

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--dataset", type=str, help="Dataset file", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--n-pages", type=int, help="Number of pages on Google News", default=2)
    parser.add_argument("--info", action='store_true', help="Show dataset informations", default=False)
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load or create dataset
    if os.path.exists(args.dataset):
        with open(args.dataset, 'r') as f:
            (urls, texts) = pickle.load(f)
            # end with
    else:
        urls = dict()
        texts = list()
    # end if

    # Show informations
    if args.info:
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

    # Load configuration file
    config = BotConfig.load(args.config)

    # Connection to MySQL
    dbc = config.get_database_config()
    mysql_connector = DBConnector(host=dbc["host"], username=dbc["username"], password=dbc["password"],
                                  db_name=dbc["database"])

    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Tweet finder
    tweet_finder = TweetFinder(shuffle=True)

    # Add RSS streams
    for rss_stream in config.get_rss_streams():
        tweet_finder.add(RSSHunter(rss_stream))
    # end for

    # Add Google News
    for news in config.get_news_config():
        for language in news['languages']:
            for country in news['countries']:
                tweet_finder.add(
                    GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country, n_pages=args.n_pages))
            # end for
        # end for
    # end for

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
            with open(args.dataset, 'w') as f:
                pickle.dump((urls, texts), f)
            # end with
        else:
            logging.debug(u"Already in stock : {}".format(tweet.get_url()))
        # end if
    # end for

# end if
