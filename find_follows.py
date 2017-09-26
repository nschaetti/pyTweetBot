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
import os
import logging
import time
import sys
import nsNLP
from friends.FriendsManager import FriendsManager
from learning.Model import Model
from learning.CensorModel import CensorModel
from executor.ActionScheduler import ActionAlreadyExists, ActionReservoirFullError
from twitter.TweetBotConnect import TweetBotConnector

####################################################
# Globals
####################################################

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Find user to follow to and add it to the DB
def find_follows(config, model, action_scheduler, features, text_size, n_pages=20):
    """
    Find tweet to like and add it to the DB
    :param config: Bot's configuration object
    :param model: Classification model's file
    :param action_scheduler: Action scheduler object
    :param features:
    :param text_size:
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

    # Unfollow interval in days
    unfollow_day = int(config.get_friends_config()['unfollow_interval'] / 86400.0)

    # Get keywords
    search_keywords = config.get_retweet_config()['keywords']

    # For each channel to research for new friends
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
                print(author.screen_name)
                print(author.description)
                print(author.friends_count)
                print(author.followers_count)
                exit()
                # Request not sent, n_following >= n_followers, description > text_size
                #if not author.follow_request_sent and
            # end for
        # end for
    # end for
# end find_follows
