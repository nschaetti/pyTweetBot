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
from twitter.TweetBotConnect import TweetBotConnector
from update_statistics import update_statistics
from tweet_finder import tweet_finder
from tweet_dataset import tweet_dataset
from tweet_training import tweet_training
from model_training import model_training
from model_testing import model_testing
from statistics_generator import statistics_generator
from list_actions import list_actions

####################################################
# Functions
####################################################


# Add default arguments
def add_default_arguments(p):
    """
    Add default arguments
    :param parser:
    :return:
    """
    # Configuration and log
    p.add_argument("--config", type=str, help="Configuration file", required=True)
    p.add_argument("--log-level", type=int, help="Log level", default=20)
# end add_default_arguments

####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(prog="pyTweetBot", description="pyTweetBot - Smart Twitter Bot")

    # Command subparser
    command_subparser = parser.add_subparsers(dest="command")

    # Update statistics parser
    update_stats_parser = command_subparser.add_parser("user-statistics")
    add_default_arguments(update_stats_parser)

    # Find tweet
    find_tweet_parser = command_subparser.add_parser("find-tweets")
    add_default_arguments(find_tweet_parser)
    find_tweet_parser.add_argument("--n-pages", type=int, help="Number of pages on Google News", default=2)
    find_tweet_parser.add_argument("--model", type=str, help="Classification model file")

    # Create data set
    train_parser = command_subparser.add_parser("train")
    add_default_arguments(train_parser)
    train_parser.add_argument("--action", type=str,
                              help="Create a data set (dataset), train or test a model (train/test)")
    train_parser.add_argument("--model", type=str, help="Path to model's file")
    train_parser.add_argument("--dataset", type=str, help="Input/output data set file")
    train_parser.add_argument("--n-pages", type=int, help="Number of pages on Google News", default=2)
    train_parser.add_argument("--rss", type=str, help="Specific RSS stream to capture", default="")
    train_parser.add_argument("--news", type=str, help="Specific Google News research to capture", default="")
    train_parser.add_argument("--info", action='store_true', help="Show information about the dataset?", default=False)
    train_parser.add_argument("--classifier", type=str, help="Classifier type (NaiveBayes, MaxEnt, TFIDF, etc)",
                              default="NaiveBayes")
    train_parser.add_argument("--param", type=float, help="Classifier parameter", default=1.0)
    train_parser.add_argument("--source", type=str,
                              help="Information source to classify (rss, news, tweets, friends, user)", required=True)

    # User's statistics
    user_statistics = command_subparser.add_parser("statistics")
    add_default_arguments(user_statistics)
    user_statistics.add_argument("--info", action='store_true', help="Show dataset informations", default=False)
    user_statistics.add_argument("--stats-file", type=str, help="Twitter statistics file")
    user_statistics.add_argument("--stream", type=str, help="Stream (timeline, user)", default="timeline")
    user_statistics.add_argument("--n-pages", type=int, help="Number of page to take into account", default=-1)

    # List command
    list_actions_parser = command_subparser.add_parser("actions")
    add_default_arguments(list_actions_parser)
    list_actions_parser.add_argument("--type", type=str, help="Action type (tweet, retweet, like, follow, unfollow",
                                     default="all")

    # List followers
    list_friends_parser = command_subparser.add_parser("friends")
    add_default_arguments(list_friends_parser)
    list_friends_parser.add_argument("--obsolete", action='store_true', help="Show only obsolete friends")
    list_friends_parser.add_argument("--friends", action='store_true', help="Show only friends")

    # Executor
    executor_parser = command_subparser.add_parser("execute")
    add_default_arguments(executor_parser)
    executor_parser.add_argument("--daemon", action='store_true', help="Run executor in daemon mode", default=False)
    executor_parser.add_argument("--break-time", action='store_true',
                                 help="Show break duration between execution for the current time", default=False)

    # Parse
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level, format='%(asctime)s :: %(levelname)s :: %(message)s')

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
    if args.command == "user-statistics":
        update_statistics(config=config)
    # Find tweets
    elif args.command == "find-tweets":
        tweet_finder(config, args.model, action_scheduler)
    # Training
    elif args.command == "train":
        # Action
        if args.action == u"dataset":
            tweet_dataset(config, args.dataset, args.n_pages, args.info, args.rss)
        elif args.action == u"test":
            model_testing(data_set_file=args.dataset, model_file=args.model)
        elif args.action == u"train":
            model_training(data_set_file=args.dataset, model_file=args.model, param=args.param, model_type=args.type)
        else:
            sys.stderr.write(u"Unknown training action {}".format(args.action))
            exit()
        # end if
    # Statistics generator
    elif args.command == "statistics":
        statistics_generator(twitter_connector, args.stats_file, args.n_pages, args.stream, args.info)
    # Executor
    elif args.command == "execute":
        #execute_actions(config, twitter_connector, action_scheduler)
        pass
    # List future action
    elif args.command == "actions":
        list_actions(action_scheduler)
    # List friends
    elif args.command == "friends":
        pass
    # Unknown command
    else:
        sys.stderr.write(u"Unknown command {}\n".format(args.command))
    # end if

# end if
