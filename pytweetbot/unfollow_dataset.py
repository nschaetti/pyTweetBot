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
            (follow, unfollow, screen_names) = pickle.load(f)
        # end with
    else:
        follow, unfollow, screen_names = list(), list(), list()
    # end if

    # Show informations
    if args.info:
        # Print info
        print(u"{} examples in the dataset".format(len(follow) + len(unfollow)))
        print(u"{} examples in the follow class".format(len(follow)))
        print(u"{} examples in the unfollow class".format(len(unfollow)))
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
    for page in twitter_connector.get_following_cursor().pages():
        # For each followers
        for friend in page:
            if friend.screen_name not in screen_names:
                print(u"Next friend to analyze: ")
                print(u"Screen name: {}".format(friend.screen_name))
                print(u"Followers count: {}".format(friend.followers_count))
                print(u"Friends count: {}".format(friend.friends_count))
                print(u"Lang: {}".format(friend.lang))
                print(u"Description: {}".format(friend.description))

                # Ask
                response = raw_input(u"Action (u(nfollow), F(ollow) : ").lower()
                print(u"")

                # Add
                if response == 'u':
                    unfollow.append(friend)
                else:
                    follow.append(friend)
                # end if

                # Save name
                screen_names.append(friend.screen_name)

                # Save
                with open(args.dataset, 'w') as f:
                    pickle.dump((follow, unfollow, screen_names), f)
                # end with
            # end with
        # end for

        # Waiting for next page
        logger.info(u"Waiting 60 seconds for next page...")
        time.sleep(60)
    # end for

# end if
