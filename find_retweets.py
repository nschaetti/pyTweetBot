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
from db.obj.Tweeted import Tweeted
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from retweet.RetweetFinder import RetweetFinder
import learning

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
def find_retweets(config, model, action_scheduler, features, text_size=80, threshold=0.5):
    """
    Find retweets and add it to the DB
    :param config:
    :param model:
    :param action_scheduler:
    :param features:
    :param text_size:
    :param threshold:
    :return:
    """
    # Retweet finders
    retweet_finders = list()

    # Get all finders
    for keyword in config.retweet['keywords']:
        retweet_finders.append(RetweetFinder(search_keywords=keyword))
    # end for

    # Load model
    tokenizer, bow, model, censor = learning.Classifier.load_model(config, model, features)

    # For each retweet finders
    for retweet_finder in retweet_finders:
        # For each tweet
        for retweet, polarity, subjectivity in retweet_finder:
            # Minimum size, not retweet, and not coming from use
            if len(retweet.text) >= text_size and retweet.text[:3] != u"RT " \
                    and retweet.screen_name == config.twitter['user']:
                # Predict class
                prediction, probs = model(bow(tokenizer(retweet.text)))
                censor_prediction, _ = censor(retweet.text)

                # Predicted as tweet
                if prediction == "pos" and censor_prediction == "pos" and not Tweeted.exists(retweet):
                    if probs['pos'] >= threshold:
                        # Try to add
                        try:
                            logging.getLogger(u"pyTweetBot").\
                            info(
                                u"Adding retweet ({}, \"{}\") to the scheduler".
                                format(
                                    retweet.id,
                                    retweet.text.encode('ascii', errors='ignore')
                                )
                            )

                            # Add action
                            action_scheduler.add_retweet(retweet.id, retweet.text)
                        except ActionReservoirFullError:
                            logging.getLogger(u"pyTweetBot").error(u"Reservoir full for Retweet action, exiting...")
                            exit()
                            pass
                        except ActionAlreadyExists:
                            logging.getLogger(u"pyTweetBot").error(u"Retweet \"{}\" already exists in the database".format(
                                retweet.text.encode('ascii', errors='ignore')))
                            pass
                        # end try
                    # end if
                # end if
            # end if
        # end for
    # end for
# end find_retweets
