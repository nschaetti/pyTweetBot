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
import sys
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from executor.ActionScheduler import ActionScheduler
from friends.FriendsManager import FriendsManager
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from twitter.TweetBotConnect import TweetBotConnector
from twitter.TweetGenerator import TweetGenerator
from update_statistics import update_statistics
from tweet_finder import tweet_finder
from tweet_dataset import tweet_dataset
from statistics_generator import statistics_generator
from list_actions import list_actions

####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument('command', type=str, nargs='?', help="Command (update_statistics, find-tweet, tweet-dataset, statistics-generator)")
    parser.add_argument("--config", type=str, help="Configuration file")
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    parser.add_argument("--dataset", type=str, help="Dataset file")
    parser.add_argument("--n-pages", type=int, help="Number of pages on Google News", default=2)
    parser.add_argument("--info", action='store_true', help="Show dataset informations", default=False)
    parser.add_argument("--rss", type=str, help="RSS stream to learn from", default="")
    parser.add_argument("--model", type=str, help="Classification model file")
    parser.add_argument("--file", type=str, help="Output file")
    parser.add_argument("--stream", type=str, help="Stream (timeline, user)", default="timeline")
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

    # Test command
    # Update statistics
    if args.command == "update-statistics":
        update_statistics(config=config)
    # Find tweets
    elif args.command == "find-tweet":
        tweet_finder(config, args.model, action_scheduler)
    # Retweet dataset
    elif args.command == "tweet-dataset":
        tweet_dataset(config, tweet_connector=twitter_connector)
    # Statistics generator
    elif args.command == "statistics-generator":
        statistics_generator(config, mysql_connector, twitter_connector)
    # Executor
    elif args.command == "execute":
        #execute_actions(config, twitter_connector, action_scheduler)
        pass
    # List future action
    elif args.command == "list":
        list_actions(action_scheduler)
    # Unknown command
    else:
        sys.stderr.write(u"Unknown command {}\n".format(args.command))
    # end if

# end if
