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
import sys
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from retweet.RetweetFinder import RetweetFinder
from twitter.TweetBotConnect import TweetBotConnector
import pickle
import time
from learning.Dataset import Dataset

####################################################
# Main function
####################################################


# Create a dataset or add data from a list of Twitter users
def follower_dataset(twitter_connect, dataset_file, info, source='followers', text_size=50):
    """
    Create a dataset or add data from a list of Twitter users.
    :param dataset_file:
    :param info:
    :return:
    """
    # Load or create dataset
    if os.path.exists(dataset_file):
        print(u"Opening dataset file {}".format(dataset_file))
        dataset = Dataset.load(dataset_file)
    else:
        dataset = Dataset()
    # end if

    # Show informations
    if info:
        print(dataset)
        exit()
    # end if

    # Get the cursor
    if source == 'followers':
        cursor = twitter_connect.get_followers_cursor()
    elif source == 'following':
        cursor = twitter_connect.get_following_cursor()
    else:
        sys.stderr.write(u"Unknown source {}\n".format(source))
        exit()
    # end if

    # For each page
    for page in cursor.pages():
        # For each user
        for user in page:
            # Minimum text length
            if len(user.description) >= text_size and not dataset.is_in(user.description):
                # Ask
                print(u"Would you classify the following element as negative(n) or positive(p)?")
                print(u"Text : {}".format(user.description))
                observed = raw_input(u"Positive or negative (p/n) (q for quit, s for skip) : ").lower()

                # Add as example
                if observed == 'q':
                    break
                elif observed == 'p':
                    dataset.add_positive(user.description)
                elif observed == 's':
                    pass
                else:
                    dataset.add_negative(user.description)
                # end if

                # Save dataset
                dataset.save(dataset_file)
            # end if
        # end for

        # Wait 1 minutes for the next page
        print(u"Waiting 1 minutes for the next page (Twitter rate limit)")
        time.sleep(60)
    # end for

# end if
