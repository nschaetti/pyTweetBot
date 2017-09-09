#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : Find tweets directly in Twitter's hashtags feeds to retweet.
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
import logging
import sys
import os
import time
from db.obj.Tweeted import Tweeted
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from retweet.RetweetFinder import RetweetFinder
from learning.Model import Model
from learning.CensorModel import CensorModel

####################################################
# Globals
####################################################

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Find retweets and add it to the DB
def find_retweets(config, model, action_scheduler):
    """
    Find retweets and add it to the DB
    :param config: Bot's configuration object
    :param model: Classification model's file
    :param action_scheduler: Action scheduler object
    :return: Number of retweets added.
    """
    # Retweet finders
    retweet_finders = list()

    # Get all finders
    for keyword in config.get_retweet_config()['keywords']:
        retweet_finders.append(RetweetFinder(search_keywords=keyword))
    # end for

    # Load model or create
    if os.path.exists(model):
        model = Model.load(model)
        censor = CensorModel(config)
    else:
        sys.stderr.write(u"Mode file {} does not exists\n".format(model))
        exit()
    # end if

    # For each retweet finders
    for retweet_finder in retweet_finders:
        # For each tweet
        for retweet, _, _ in retweet_finder:
            # Predict class
            prediction, = model(retweet.text)
            censor_prediction, = censor(retweet.text)

            # Predicted as tweet
            if prediction == "tweet" and censor_prediction == "tweet" and not Tweeted.exists(retweet.id):
                # Try to add
                try:
                    logging.info(u"Adding Tweet \"{}\" to the scheduler".format(
                        retweet.tweet.encode('ascii', errors='ignore')))
                    action_scheduler.add_retweet(retweet.id)
                except ActionReservoirFullError:
                    logging.error(u"Reservoir full for Retweet action, waiting for one hour")
                    time.sleep(3600)
                    pass
                except ActionAlreadyExists:
                    logging.error(u"Retweet \"{}\" already exists in the database".format(
                        retweet.text.encode('ascii', errors='ignore')))
                    pass
                # end try
            # end if
        # end for
    # end for

# end find_retweets
