#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : executor.ExecutorThread.py
# Description : Execute actions.
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
from friends.FriendsManager import ActionAlreadyDone
from twitter.TweetBotConnect import RequestLimitReached
import logging
import tweepy
from threading import Thread, Lock

# Mutex
mutex = Lock()


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
                self._wait_next_action()
            # end if
        # end while
    # end run

    ##############################################
    # Private
    ##############################################

    # Wait next action
    def _wait_next_action(self):
        """
        Wait for the next action
        :return:
        """
        # Wait
        if self._action_type == "Follow":
            self._config.wait_next_action("follow")
        elif self._action_type == "Unfollow":
            self._config.wait_next_action("unfollow")
        elif self._action_type == "Retweet":
            self._config.wait_next_action("retweet")
        elif self._action_type == "Like":
            self._config.wait_next_action("like")
        elif self._action_type == "Tweet":
            self._config.wait_next_action("tweet")
        # end if
    # end wait_next_action

    ##############################################
    # Override
    ##############################################

    # Execute the next action
    def __call__(self):
        """
        Execute the next action
        """
        # Try to execute
        try:
            # Lock
            with mutex:
                # Get next action
                action = self._scheduler.next_action_to_execute(self._action_type)

                # Execute if found
                if action is not None:
                    # Execute
                    action.execute()

                    # Delete
                    self._scheduler.delete(action)
                # end if
            # end mutex

            # Wait
            self._wait_next_action()
        except RequestLimitReached as e:
            # Log error
            logging.getLogger(u"pyTweetBot").error(
                u"Limit reached while executing action {} : {}".format(action, e)
            )

            # Wait
            self._wait_next_action()
        except fr.ActionAlreadyDone as e:
            # Delete action
            with mutex:
                self._scheduler.delete(action)
            # end mutex

            # Log error
            logging.getLogger(u"pyTweetBot").error(
                u"Action {} already done : {}".format(action, e))
        except tweepy.TweepError as e:
            # Delete action
            with mutex:
                self._scheduler.delete(action)
            # end mutex

            # Log error
            logging.getLogger(u"pyTweetBot").error(
                u"Error while executing action {} : {}".format(action, e))
        # end try
    # end __call__

# end ExecutorThread

