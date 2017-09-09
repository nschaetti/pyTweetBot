#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : find_unfollows.py
# Description : Find user to unfollow in the DB.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 30.07.2017 17:59:05
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
import logging
import time
from friends.FriendsManager import FriendsManager
from learning.Model import Model
from learning.CensorModel import CensorModel
from executor.ActionScheduler import ActionAlreadyExists, ActionReservoirFullError

####################################################
# Globals
####################################################

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Find user to unfollow to and add it to the DB
def find_unfollows(config, model, action_scheduler):
    """
    Find tweet to like and add it to the DB
    :param config: Bot's configuration object
    :param model: Classification model's file
    :param action_scheduler: Action scheduler object
    :return: Number of retweets added.
    """
    # Friends manager
    friends_manager = FriendsManager()

    # Load model or create
    if os.path.exists(model):
        model = Model.load(model)
        censor = CensorModel(config)
    else:
        logging.fatal(u"Model file {} does not exists".format(args.model))
        exit()
    # end if

    # First unfollow obsolete friends
    for friend in friends_manager.get_obsolete_friends():
        try:
            logging.info(
                u"Adding obsolete Friend \"{}\" to unfollow to the scheduler".format(friend.friend_screen_name))
            action_scheduler.add_unfollow(friend.friend_screen_name)
        except ActionReservoirFullError:
            logging.error(u"Reservoir full for Unfollow action, waiting for one hour")
            time.sleep(3600)
            pass
        except ActionAlreadyExists:
            logging.error(
                u"Unfollow action for \"{}\" already exists in the database".format(friend.friend_screen_name))
            pass
        # end try
    # end for

    # Find friends to unfollow
    """for page in twitter_connector.get_following_cursor().pages():
        # For each followers
        for friend in page:
            # Predict class
            prediction, = model(friend)

            # Predicted as unfollow
            if prediction == "unfollow":
                try:
                    logging.info(u"Adding Friend \"{}\" to unfollow to the scheduler".format(friend.friend_screen_name))
                    action_scheduler.add_unfollow(friend.friend_screen_name)
                except ActionReservoirFullError:
                    logging.error(u"Reservoir full for Unfollow action, waiting for one hour")
                    time.sleep(3600)
                    pass
                except ActionAlreadyExists:
                    logging.error(
                        u"Unfollow action for \"{}\" already exists in the database".format(friend.friend_screen_name))
                    pass
                # end try
            # end if
        # end for
    # end for"""
# end find_follows
