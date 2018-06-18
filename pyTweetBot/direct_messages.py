#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : find_tweet.py
# Description : Find new tweets from various sources
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
import time
from twitter.TweetBotConnect import TweetBotConnector
from friends.FriendsManager import FriendsManager
from db.DBConnector import DBConnector
import tools.strings as pystr

####################################################
# Globals
####################################################


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


def direct_messages(config):
    """This function send direct messages to followers
    if they have not been contacted before.

    Example:
        >>> config = BotConfig.load("config.json")
        >>> direct_messages(config)

    Arguments:
        config (BotConfig): Bot configuration object of type :class:`pyTweetBot.config.BotConfig`
    """
    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Friends
    friends_manager = FriendsManager()

    # DB connector
    mysql_connector = DBConnector()

    # Direct message
    msg = config.direct_message

    # Get friend to contact
    for friend in friends_manager.get_uncontacted_friends():
        # Send direct message
        twitter_connector.send_direct_message(text=msg, screen_name=friend.friend_screen_name)

        # Set as contacted
        friend.friend_contacted = True

        # Commit
        mysql_connector.get_session().commit()

        # Wait
        logging.getLogger(pystr.LOGGER).info(pystr.INFO_TWITTER_WAIT)
        time.sleep(60)
    # end for
# end if
