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
import sys
import nsNLP
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
def find_unfollows(config, friends_manager, model, action_scheduler, features):
    """
    Find tweet to like and add it to the DB
    :param config: Bot's configuration object
    :param model: Classification model's file
    :param action_scheduler: Action scheduler object
    :return: Number of retweets added.
    """
    # Load model
    if model is not None and os.path.exists(model):
        model = nsNLP.classifiers.TextClassifier.load(model)
        censor = CensorModel(config)
    else:
        sys.stderr.write(u"Can't open model file {}\n".format(model))
        exit()
    # end if

    # Tokenizer
    tokenizer = nsNLP.tokenization.NLTKTokenizer(lang='english')

    # Parse features
    feature_list = features.split('+')

    # Join features
    bow = nsNLP.features.BagOfGrams()

    # For each features
    for bag in feature_list:
        # Select features
        if bag == 'words':
            b = nsNLP.features.BagOfWords()
        elif bag == 'bigrams':
            b = nsNLP.features.BagOf2Grams()
        elif bag == 'trigrams':
            b = nsNLP.features.BagOf3Grams()
        else:
            sys.stderr.write(u"Unknown features type {}\n".format(bag))
            exit()
        # end if
        bow.add(b)
    # end for

    # First unfollow obsolete friends
    logging.getLogger(u"pyTweetBot").info(u"Searching obsolete friends to unfollow")
    for friend in friends_manager.get_obsolete_friends():
        try:
            logging.getLogger(u"pyTweetBot").info(
                u"Adding obsolete Friend \"{}\" to unfollow to the scheduler".format(friend.friend_screen_name))
            action_scheduler.add_unfollow(friend.friend_screen_name)
        except ActionReservoirFullError:
            logging.getLogger(u"pyTweetBot").error(u"Reservoir full for Unfollow action, waiting for one hour")
            time.sleep(3600)
            pass
        except ActionAlreadyExists:
            logging.getLogger(u"pyTweetBot").error(
                u"Unfollow action for \"{}\" already exists in the database".format(friend.friend_screen_name))
            pass
        # end try
    # end for

    # Find friends to unfollow
    logging.getLogger(u"pyTweetBot").info(u"Searching useless friends to unfollow")
    for friend in friends_manager.get_following():
        if not FriendsManager.is_follower(friend.friend_screen_name):
            # Predict class
            prediction, = model(bow(tokenizer(friend.friend_description)))
            censor_prediction, _ = censor(friend.friend_description)

            # Predicted as unfollow
            if prediction == 'neg' or censor_prediction == 'neg':
                try:
                    logging.getLogger(u"pyTweetBot").info(
                        u"Adding Friend \"{}\" to unfollow to the scheduler".format(friend.friend_screen_name))
                    action_scheduler.add_unfollow(friend.friend_screen_name)
                except ActionReservoirFullError:
                    logging.getLogger(u"pyTweetBot").error(u"Reservoir full for unfollow action, exiting...")
                    exit()
                    pass
                except ActionAlreadyExists:
                    logging.getLogger(u"pyTweetBot").error(
                        u"Unfollow action for \"{}\" already exists in the database".format(friend.friend_screen_name))
                    pass
                # end try
            # end if
        # end if
    # end for
# end find_follows
