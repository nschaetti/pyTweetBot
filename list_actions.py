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


# List actions
def list_actions(action_scheduler):
    """
    List actions
    :return:
    """
    # Get actions
    actions = action_scheduler.list_actions()

    # For each action
    for action in actions:
        if action.action_type == 'tweet':
            print(u"[{}] will tweet \"{}\"".format(action.action_tweet_text))
        # end if
    # end for
# end list_actions
