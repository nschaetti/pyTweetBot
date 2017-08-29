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
import time

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
    parser.add_argument("--info", action='store_true', help="Show dataset informations", default=False)
    parser.add_argument("--search", type=str, help="Research term if needed", default="")
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load or create dataset
    if os.path.exists(args.dataset):
        with open(args.dataset, 'r') as f:
            tweets = pickle.load(f)
        # end with
    else:
        tweets = dict()
    # end if

    # Show informations
    if args.info:
        # Compute statistics
        examples_count = len(tweets.keys())
        retweet_count = 0
        skip_count = 0
        for tweet in tweets.keys():
            if tweets[tweet] == "tweet":
                retweet_count += 1
            else:
                skip_count += 1
                # end if
        # end for

        # Print info
        print(u"{} examples in the dataset".format(examples_count))
        print(u"{} examples in the retweet class".format(retweet_count))
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

    # Retweet finder
    retweet_finder = RetweetFinder(search_keywords=args.search, languages=['en', 'fr'], polarity=-1, subjectivity=1)

    # For each tweet
    for tweet, polarity, subjectivity in retweet_finder:
        if tweet.text not in tweets.keys() and not tweet.retweeted:
            # Ask
            print(tweet.text)
            print(u"Polarity : {}".format(polarity))
            print(u"Subjectivity : {}".format(subjectivity))
            observed = raw_input("ReTweet or Skip (t/S/e)? ").lower()

            # Add as example
            if observed == "e":
                break
            elif observed == "t":
                tweets[tweet.text] = "tweet"
            else:
                tweets[tweet.text] = "skip"
            # end if

            # Save dataset
            with open(args.dataset, 'w') as f:
                pickle.dump(tweets, f)
            # end with
        else:
            logging.debug(u"Already in stock : {}".format(tweet.text))
        # end if
    # end if

# end if
