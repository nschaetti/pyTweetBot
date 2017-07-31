#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot unfollow dataset creator.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 30.07.2017 08:58:00
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

    # For each followers page
    for page in twitter_connector.get_followers_cursor().pages():
        # For each followers
        for follower in page:
            print(follower)
        # end for
        time.sleep(60)
    # end for

    # Retweet finder
    retweet_finder = RetweetFinder(search_keywords=args.search, languages=['en', 'fr'], polarity=-1, subjectivity=1)

# end if
