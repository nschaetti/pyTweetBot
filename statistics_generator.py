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
from config.BotConfig import BotConfig
from twitter.TweetBotConnect import TweetBotConnector

####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--n_pages", type=int, help="Number of page to take into account", default=100)
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load configuration file
    config = BotConfig.load(args.config)

    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Stats for each day of the week
    week_day_stats = dict()

    # For each of my tweets
    for page in twitter_connector.get_user_timeline(screen_name="nschaetti", n_pages=args.n_pages):
        # For each tweet
        for tweet in page:
            if not tweet.retweeted:
                print(tweet)
                exit()
                print(tweet.created_date)
                print(tweet.retweet_count * 2 + tweet.favorite_count)
                print("")
            # end if
        # end for

        # Wait
        time.sleep(60)
    # end for

# end if
