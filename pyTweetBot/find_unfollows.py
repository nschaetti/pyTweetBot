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
# along with pyTweetBot.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
import logging
import os
import pickle
import learning
import tools.strings as pystr
from executor.ActionScheduler import ActionAlreadyExists, ActionReservoirFullError
import tools.strings as pystr


# Find user to unfollow to and add it to the DB
def find_unfollows(config, friends_manager, model_file, action_scheduler, threshold=0.5):
    """Find Twitter users to unfollow according to the parameters in the configuration file.

    Example:
        >>> config = BotConfig.load("config.json")
        >>> action_scheduler = ActionScheduler(config=config)
        >>> friends_manager = FriendsManager()
        >>> find_unfollows(config, friends_manager, "model.p", action_scheduler)

    Arguments:
        * config (BotConfig): Bot configuration object of type :class:`pyTweetBot.config.BotConfig`
        * friends_manager (FriendsManager): Friend manager object of type :class:`pyTweetBot.friends.FriendsManager`
        * model_file (str): Path to the model's Pickle file.
        * action_scheduler (ActionScheduler): Action scheduler object.
        * threshold (float): Probability threshold to accept unfollow.
    """
    # Load censor
    censor = learning.CensorModel.load_censor(config)

    # Load model
    if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
    else:
        logging.getLogger(pystr.LOGGER).error(pystr.ERROR_CANNOT_FIND_MODEL.format(model_file))
        exit()
        # end if

    # Unfollow interval in days
    unfollow_day = int(config.friends['unfollow_interval'] / 86400.0)

    # First find friends who are not following back after defined period
    logging.getLogger(pystr.LOGGER).info(pystr.INFO_RESEARCHING_OBSOLETE_FRIENDS)
    for friend in friends_manager.get_obsolete_friends(unfollow_day):
        try:
            logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_UNFOLLOW_SCHEDULER.format(friend.friend_screen_name))
            action_scheduler.add_unfollow(friend.friend_screen_name)
        except ActionReservoirFullError:
            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL_UNFOLLOW)
            exit()
            pass
        except ActionAlreadyExists:
            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_UNFOLLOW_ALREADY_DB.format(friend.friend_screen_name))
            pass
        # end try
    # end for

    # Find friends to unfollow (because they don't follow back and they don't meet our criterias)
    logging.getLogger(pystr.LOGGER).info(pystr.INFO_RESEARCHING_USELESS_FRIENDS)
    for friend in friends_manager.get_following():
        if not friend.friend_follower:
            # Predict class
            prediction = model.predict([friend.friend_description])[0]
            probs = model.predict_proba([friend.friend_description])[0]
            censor_prediction, _ = censor(friend.friend_description)

            # Predicted as unfollow
            if prediction == 'neg' or censor_prediction == 'neg' or probs[1] < threshold:
                try:
                    logging.getLogger(pystr.LOGGER).info(pystr.INFO_ADD_UNFOLLOW_SCHEDULER.format(friend.friend_screen_name))
                    action_scheduler.add_unfollow(friend.friend_screen_name)
                except ActionReservoirFullError:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL_UNFOLLOW)
                    exit()
                    pass
                except ActionAlreadyExists:
                    logging.getLogger(pystr.LOGGER).error(pystr.ERROR_UNFOLLOW_ALREADY_DB.format(friend.friend_screen_name))
                    pass
                # end try
            # end if
        # end if
    # end for
# end find_follows
