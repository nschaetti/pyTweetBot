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
import time
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
from twitter.TweetBotConnect import TweetBotConnector
from db.obj.ImpactStatistics import ImpactStatistic
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector

####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--file", type=str, help="Output file", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--n-pages", type=int, help="Number of page to take into account", default=-1)
    parser.add_argument("--stream", type=str, help="Stream (timeline, user)", default=10)
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

    # Stats for each day of the week
    if not os.path.exists(args.file):
        week_day_stats = np.zeros((7, 24))
    else:
        week_day_stats = pickle.load(open(args.file, 'r'))
    # end if

    # Cursor
    if args.stream == "timeline":
        cursor = twitter_connector.get_time_line(n_pages=args.n_pages)
    else:
        cursor = twitter_connector.get_user_timeline(screen_name="nschaetti", n_pages=args.n_pages)
    # end if

    # Week day index to string
    week_to_string = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # For each of my tweets
    for index, page in enumerate(cursor):
        logger.info(u"Analyzing page number {}".format(index))

        # For each tweet
        for tweet in page:
            if not tweet.retweeted:
                print(tweet.created_at.weekday())
                print(tweet.created_at.hour)
                print(tweet.retweet_count * 2 + tweet.favorite_count)
                week_day_stats[
                    tweet.created_at.weekday(), tweet.created_at.hour] += tweet.retweet_count * 2 + tweet.favorite_count
            # end if
        # end for

        # Save matrix
        pickle.dump(week_day_stats, open(args.file, 'w'))

        # Wait
        logger.info(u"Waiting 60 seconds...")
        time.sleep(60)
    # end for

# end if
