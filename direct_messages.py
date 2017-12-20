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
from twitter.TweetBotConnect import TweetBotConnector
from friends.FriendsManager import FriendsManager

####################################################
# Globals
####################################################


####################################################
# Functions
####################################################


####################################################
# Main function
####################################################


# Send direct message to new followers
def direct_messages(config):
    """
    Send direct messages to new followers
    :param config:
    :return:
    """
    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Friends
    friends_manager = FriendsManager()

    # Direct message
    msg = config.direct_message

    # Get friend to contact
    for friend in friends_manager.get_uncontacted_friends():
        # Send direct message
        twitter_connector.send_direct_message(msg, friend.friend_screen_name)

        # Set as contacted
        friend.friend_contacted = True
        exit()
    # end for
# end if
