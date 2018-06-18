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
import os
import sys
from twitter.TweetBotConnect import TweetBotConnector
import time
from learning.Dataset import Dataset
import tools.strings as pystr


# Create a dataset or add data from a list of Twitter users
def follower_dataset(twitter_connect, dataset_file, info, source='followers', text_size=50):
    """Create a dataset or add textual data from a list of Twitter users.

    Example:
        >>> config = BotConfig.load("config.json")
        >>> twitter_connector = TweetBotConnector(config)
        >>> follower_dataset(twitter_connect, "dataset.p", False, 'followers')

    Arguments:
        * twitter_connect (TweetBotConnector): Twitter bot connector object of type :class:`pyTweetBot.twitter.TweetBotConnect`
        * dataset_file (str): Path to the dataset file to load or create.
        * info (bool): If True, show information about the dataset and exit
        * source (str): Can be 'follower' or 'following'. Set where to load users from.
        * text_size (int): Minimum user's description length to take the profile into account.
    """
    # Load or create dataset
    if os.path.exists(dataset_file):
        print(pystr.INFO_OPENING_DATASET_FILE.format(dataset_file))
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
        sys.stderr.write(pystr.ERROR_UNKNOWN_SOURCE.format(source))
        exit()
    # end if

    # For each page
    for page in cursor.pages():
        # For each user
        for user in page:
            # Minimum text length
            if len(user.description) >= text_size and not dataset.is_in(user.description):
                # Ask
                print(pystr.DIALOG_CLASS_LABEL)
                print(pystr.DIALOG_USER_DESCRIPTION.format(user.description))
                observed = raw_input(pystr.DIALOG_INPUT_CLASS_LABEL).lower()

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
        print(pystr.INFO_TWITTER_WAIT)
        time.sleep(60)
    # end for

# end if
