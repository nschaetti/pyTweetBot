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
import nltk
from urllib import urlopen
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from executor.ActionScheduler import ActionScheduler, ActionReservoirFullError, ActionAlreadyExists
from friends.FriendsManager import FriendsManager
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from twitter.TweetBotConnect import TweetBotConnector
from twitter.TweetGenerator import TweetGenerator
from tweet.TweetFactory import TweetFactory
from learning.Model import Model
from learning.StatisticalModel import StatisticalModel

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
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
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

    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Friends
    friends_manager = FriendsManager()

    # Action scheduler
    action_scheduler = ActionScheduler()

    # Tweet factory
    tweet_factory = TweetFactory(config.get_hashtags())
    action_scheduler.set_factory(tweet_factory)

    # Tweet finder
    tweet_finder = TweetFinder()

    # Create or get model
    """if not Model.exists("stats_model_for_tweet"):
        model = StatisticalModel.create("stats_model_for_tweet", 2)
    else:
        model = StatisticalModel.load("stats_model_for_tweet")
    # end if"""

    # Create or get model
    if os.path.exists(args.model):
        model = StatisticalModel.load_from_file(args.model)
    else:
        model = StatisticalModel(name="stats_model_for_tweet", classes=["tweet", "skip"], tokens_probs=None,
                                 last_update=datetime.datetime.utcnow())
    # end if

    # Add RSS streams
    for rss_stream in config.get_rss_streams():
        tweet_finder.add(RSSHunter(rss_stream))
    # end for

    # Add Google News
    for news in config.get_news_config():
        for language in news['languages']:
            for country in news['countries']:
                tweet_finder.add(GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country))
            # end for
        # end for
    # end for

    # Init test stats
    if args.test:
        total = 0
        success = 0
    # end if

    # For each tweet
    for tweet in tweet_finder:
        # Get URL's text
        text = nltk.clean_html(urlopen(tweet.get_url()).read())

        # Ask
        print(tweet.get_text())
        print(tweet.get_url())
        observed = raw_input("Tweet or Skip (t/S/e)? ").lower()

        # Train or test
        if not args.test:
            # Add as example
            if observed == "e":
                break
            elif observed == "s":
                model.train(text, "skip")
            elif observed == "t":
                model.train(text, "tweet")
            # end if
        else:
            # Predict
            predicted = model(text)

            # Test
            if observed == "e" or observed == "":
                break
            elif observed == "s" and predicted == "skip":
                success += 1.0
            elif observed == "t" and predicted == "tweet":
                success += 1.0
            # end if

            # Add counter
            total += 1.0
    # end for

    # Dislay stats
    if args.test:
        logging.info("Test success rate : {}".format(success / total * 100.0))
    # end if

    # Save the model
    model.save()

# end if
