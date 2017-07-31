#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot find retweet script.
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
import argparse
import logging
import signal, os
import time
from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from executor.ActionScheduler import ActionScheduler, ActionReservoirFullError, ActionAlreadyExists
from friends.FriendsManager import FriendsManager
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from retweet.RetweetFinder import RetweetFinder
from twitter.TweetBotConnect import TweetBotConnector
from tweet.TweetFactory import TweetFactory
from learning.Model import Model
from learning.CensorModel import CensorModel

####################################################
# Globals
####################################################

# Continue main loop?
cont_loop = True

####################################################
# Functions
####################################################


# Signal handler
def signal_handler(signum, frame):
    """
    Signal handler
    :param signum:
    :param frame:
    :return:
    """
    global cont_loop
    logging.info(u"Signal {} received in frame {}".format(signum, frame))
    cont_loop = False
# end signal_handler


####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--model", type=str, help="Model file", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGQUIT, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load configuration file
    config = BotConfig.load(args.config)

    # Connection to MySQL
    dbc = config.get_database_config()
    mysql_connector = DBConnector(host=dbc["host"], username=dbc["username"], password=dbc["password"],
                                  db_name=dbc["database"])

    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Action scheduler
    action_scheduler = ActionScheduler()

    # Tweet factory
    tweet_factory = TweetFactory(config.get_hashtags())
    action_scheduler.set_factory(tweet_factory)

    # Retweet finders
    retweet_finders = list()

    # Get all finders
    for keyword in config.get_retweet_config()['keywords']:
        retweet_finders.append(RetweetFinder(search_keywords=keyword))
    # end for

    # Load model or create
    if os.path.exists(args.model):
        model = Model.load(args.model)
        censor = CensorModel(config)
    else:
        logging.error(u"Mode file {} does not exists".format(args.model))
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
            if prediction == "tweet" and censor_prediction == "tweet" and not tweet.already_tweeted():
                # Try to add
                try:
                    logging.info(u"Adding Tweet \"{}\" to the scheduler".format(
                        tweet.get_tweet().encode('ascii', errors='ignore')))
                    action_scheduler.add_tweet(tweet)
                except ActionReservoirFullError:
                    logging.error(u"Reservoir full for Tweet action, waiting for one hour")
                    time.sleep(3600)
                    pass
                except ActionAlreadyExists:
                    logging.error(u"Tweet \"{}\" already exists in the database".format(
                        tweet.get_tweet().encode('ascii', errors='ignore')))
                    pass
                # end try
            # end if
        # end for
    # end for

# end if
