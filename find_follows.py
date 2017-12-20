#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : find_follows.py
# Description : Find users to follow based on their description.
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
import tweepy
import logging
import time
import random
import db.obj
import learning
from executor.ActionScheduler import ActionAlreadyExists, ActionReservoirFullError
from twitter.TweetBotConnect import TweetBotConnector

####################################################
# Globals
####################################################

####################################################
# Functions
####################################################


# Add follow action
def add_follow_action(action_scheduler, friend):
    """
    Add follow action
    :param action_scheduler: Action scheduler object
    :param friend: Friend to add as a db.obj.Friend or tweepy.User object
    :return:
    """
    try:
        if type(friend) is db.obj.Friend:
            logging.getLogger(u"pyTweetBot").info(
                u"Adding Friend \"{}\" to follow to the scheduler".format(friend.friend_screen_name))
            action_scheduler.add_follow(friend.friend_screen_name)
        elif type(friend) is tweepy.User:
            logging.getLogger(u"pyTweetBot").info(
                u"Adding Friend \"{}\" to follow to the scheduler".format(friend.screen_name))
            action_scheduler.add_follow(friend.screen_name)
        # end if
    except ActionReservoirFullError:
        logging.getLogger(u"pyTweetBot").error(u"Reservoir full for follow action, exiting...")
        exit()
        pass
    except ActionAlreadyExists:
        if type(friend) is db.obj.Friend:
            logging.getLogger(u"pyTweetBot").error(
                u"Follow action for \"{}\" already exists in the database".format(
                    friend.friend_screen_name))
        elif type(friend) is tweepy.User:
            logging.getLogger(u"pyTweetBot").error(
                u"Follow action for \"{}\" already exists in the database".format(
                    friend.screen_name))
        # end if
        pass
    # end try
# end add_follow_action

####################################################
# Main function
####################################################


# Find user to follow to and add it to the DB
def find_follows(config, model, action_scheduler, friends_manager, text_size, n_pages=20, threshold=0.5):
    """
    Find tweet to like and add it to the DB
    :param config: Bot's configuration object
    :param model: Classification model's file
    :param action_scheduler: Action scheduler object
    :param friends_manager: Friends manager object
    :param text_size: Minimum text size to be accepted
    :param n_pages: Number of pages to search for each term
    :param threshold: Minimum probability to accept following
    """
    # Load model
    tokenizer, bow, model, censor = learning.Classifier.load_model(config, model)

    # For each followers
    for follower in friends_manager.get_followers():
        # He follows me, but I don't
        if not follower.friend_following:
            # Censor prediction
            censor_prediction, _ = censor(follower.friend_description)

            # If positive prediction
            if censor_prediction == 'pos':
                # Add
                add_follow_action(action_scheduler, follower)
            # end if
        # end if
    # end for

    # Get options
    search_keywords = config.retweet['keywords']
    ratio = config.friends['ratio']

    # Shuffle keywords
    random.shuffle(search_keywords)

    # For each channel research for new friends
    for search_keyword in search_keywords:
        # Log
        logging.getLogger(u"pyTweetBot").info(u"Search new possible friends in the stream {}".format(search_keyword))

        # Research this keyword
        cursor = TweetBotConnector().search_tweets(search_keyword, n_pages)

        # For each pages
        for page in cursor:
            # For each tweet
            for tweet in page:
                # Tweet's author
                author = tweet.author

                # Request not sent, n_following >= n_followers, description > text_size
                if not author.follow_request_sent and author.friends_count >= (author.followers_count * ratio) and len(author.description) > text_size:
                    # Predict class
                    prediction, probs = model(bow(tokenizer.tokenize(author.description)))
                    censor_prediction, _ = censor(author.description)

                    # Predicted as follow
                    if prediction == 'pos' and censor_prediction == 'pos' and probs['pos'] >= threshold:
                        # Add
                        add_follow_action(action_scheduler, author)
                    # end if
                # end if
            # end for

            # Wait 1 minute
            logging.getLogger(u"pyTweetBot").info(u"Waiting for 1 minute (Twitter limits)")
            time.sleep(60)
        # end for
    # end for
# end find_follows
