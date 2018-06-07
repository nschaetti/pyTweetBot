#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : find_retweets.py
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
import os
import pickle
import learning
import tools.strings as pystr
from db.obj.Tweeted import Tweeted
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from retweet.RetweetFinder import RetweetFinder


# Find retweets and add it to the DB
def find_retweets(config, model_file, action_scheduler, text_size=80, threshold=0.5):
    """Find tweets to retweet from search terms set in the config file.

    Example:
        >>> config = BotConfig.load("config.json")
        >>> action_scheduler = ActionScheduler(config=config)
        >>> find_retweets(config, "model.p", action_scheduler)

    Arguments:
        * config (BotConfig): Bot configuration object of type :class:`pyTweetBot.config.BotConfig`
        * model_file (str): Path to the file containing the classifier model
        * action_scheduler (ActionScheduler): Action scheduler object of type :class:`pyTweetBot.executor.ActionScheduler`
        * text_size (int): Minimum text length to take a tweet into account
        * threshold (float): Minimum to reach to be classified as positive
    """
    # Retweet finders
    retweet_finders = list()

    # Get all finders
    for keyword in config.retweet['keywords']:
        retweet_finders.append(RetweetFinder(search_keywords=keyword))
    # end for

    # Load censor
    censor = learning.CensorModel.load_censor(config)

    # Load model
    if os.path.exists(model_file):
        model = pickle.load(open(model_file, 'rb'))
    else:
        logging.getLogger(pystr.LOGGER).error(pystr.ERROR_CANNOT_FIND_MODEL.format(model_file))
        exit()
    # end if

    # For each retweet finders
    for retweet_finder in retweet_finders:
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Changing hunter to {}".format(retweet_finder))

        # For each tweet
        for retweet, polarity, subjectivity in retweet_finder:
            # Minimum size, not retweet, and not coming from use
            if len(retweet.text) >= text_size and retweet.text[:3] != u"RT " \
                    and retweet.author.screen_name != config.twitter['user']:
                # Predict class
                prediction = model.predict([retweet.text])[0]
                probs = model.predict_proba([retweet.text])[0]
                censor_prediction, _ = censor(retweet.text)

                # Predicted as tweet
                if prediction == "pos" and censor_prediction == "pos" and not Tweeted.exists(retweet):
                    if probs[1] >= threshold:
                        # Try to add
                        try:
                            logging.getLogger(pystr.LOGGER).\
                            info(
                                pystr.INFO_ADD_RETWEET_SCHEDULER.
                                format(
                                    retweet.id,
                                    retweet.text.encode('ascii', errors='ignore')
                                )
                            )

                            # Add action
                            action_scheduler.add_retweet(retweet.id, retweet.text)
                        except ActionReservoirFullError:
                            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RESERVOIR_FULL)
                            exit()
                            pass
                        except ActionAlreadyExists:
                            logging.getLogger(pystr.LOGGER).error(pystr.ERROR_RETWEET_ALREADY_DB.format(
                                retweet.text.encode('ascii', errors='ignore')))
                            pass
                        # end try
                    # end if
                # end if
            # end if
        # end for
    # end for
# end find_retweets
