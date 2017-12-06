#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : executor/ActionScheduler.py
# Description : Manage bot's actions.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 15.06.2017 18:14:00
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

# Imports
import sqlalchemy
import datetime
from datetime import timedelta
import db
import db.obj
from config.BotConfig import BotConfig
from friends.FriendsManager import FollowUnfollowRatioReached
from twitter.TweetBotConnect import TweetBotConnector
from sqlalchemy import and_
import logging
from patterns.singleton import singleton
import tweepy
from threading import Thread
import random
import sys


# Execute actions in a thread
class ExecutorThread(Thread):
    """
    Execute actions in a thread
    """

    # Constuctor
    def __init__(self, config, scheduler, action_type):
        """
        Constructor
        :param config: BotConfig object containing bot configuration
        :param scheduler: ActionScheduler object
        :param action_type: Which type of action the thread must execute
        """
        # Properties
        self._scheduler = scheduler
        self._action_type = action_type
        self._config = config

        # Tread
        Thread.__init__(self)
    # end __init__

    ##############################################
    # Public
    ##############################################

    # Thread running function
    def run(self):
        """
        Thread running function
        :return:
        """
        # Main loop
        while True:
            # Execute actions if awake or wait
            if self._config.is_awake():
                self()
            else:
                self._config.wait_next_action()
            # end if
        # end while
    # end run

    ##############################################
    # Override
    ##############################################

    # Execute the next action
    def __call__(self):
        """
        Execute the next action
        """
        """
                Execute action
                :return:
                """
        # Action to execute
        action_to_execute = list()
        n_action = 0

        # Get action to be executed
        action = self._scheduler._get_exec_action(self._action_type)

            # Try to execute
            try:
                # Execute
                action.execute()

                # Delete action
                self.delete(action)
                action_to_execute.remove(action)

                # Wait
                self._config.wait_next_action()
            except FollowUnfollowRatioReached as e:
                # Log error
                logging.getLogger(u"pyTweetBot").error(
                    u"Error while executing action {} : {}".format(action, e)
                )
            except tweepy.TweepError as e:
                # Delete action
                self.delete(action)
                action_to_execute.remove(action)

                # Log error
                logging.getLogger(u"pyTweetBot").error(
                    u"Error while executing action {} : {}".format(action, e))
            # end try
    # end __call__

# end ExecutorThread

