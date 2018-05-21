#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
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
import threading
from Queue import Queue
from config.BotConfig import BotConfig
from executor.ExecutorThread import ExecutorThread
import tools.strings as pystr
import time

####################################################
# Main function
####################################################


# Execute actions
def execute_actions(config, action_scheduler, no_tweet=False, no_retweet=False, no_like=False, no_follow=False, no_unfollow=False):
    """
    Execute actions
    :param config:
    :param action_scheduler:
    :param no_tweet:
    :param no_retweet:
    :param no_like:
    :param no_follow:
    :param no_unfollow:
    :return:
    """
    # List of threads
    thread_queue = Queue()

    # Filter
    filters = {'Tweet': no_tweet, 'Retweet': no_retweet, 'Like': no_like, 'Follow': no_follow, 'Unfollow': no_unfollow}

    # Interrupt event
    run_event = threading.Event()
    run_event.set()

    # For each action type
    for action_type in action_scheduler.action_types:
        if not filters[action_type]:
            # New executor thread
            executor_thread = ExecutorThread(config, action_scheduler, action_type, run_event)

            # Start executing action
            logging.getLogger(pystr.LOGGER).info(u"Start thread for action type {}...".format(action_type))

            # Start as daemon
            executor_thread.daemon = True
            executor_thread.start()

            # Add to queue
            thread_queue.put(executor_thread)
        # end if
    # end for

    # Waiting for the thread to terminate
    try:
        while 1:
            time.sleep(1)
        # end while
    except (KeyboardInterrupt, SystemExit):
        # Log
        logging.getLogger(pystr.LOGGER).info(u"Stopping executing action with scheduler...")

        # Clear event
        run_event.clear()

        # Join
        thread_queue.join()
    # end try
# end execute_actions
