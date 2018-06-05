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
import sys


# List actions
def list_actions(action_scheduler, action_type=""):
    """
    List actions
    :param action_scheduler: Action Scheduler object
    :param action_type: Filter action type
    """
    # Get actions
    actions = action_scheduler.list_actions(action_type=action_type)

    # Counters
    total_action = 0
    n_actions = {'Tweet': 0, 'Retweet': 0, 'Like': 0, 'Follow': 0, 'Unfollow': 0}

    # For each action
    for action in actions:
        if action.action_type == 'Tweet':
            sys.stdout.write(u"[{}] will tweet \"{}\"\n".format(action.action_id, action.action_tweet_text))
        elif action.action_type == 'Retweet':
            sys.stdout.write(u"[{}] will retweet {}\n".format(action.action_id, action.action_tweet_id))
        elif action.action_type == 'Like':
            sys.stdout.write(u"[{}] will like {}\n".format(action.action_id, action.action_tweet_id))
        elif action.action_type == 'Follow':
            sys.stdout.write(u"[{}] will follow \"{}\"\n".format(action.action_id, action.action_tweet_text))
        elif action.action_type == 'Unfollow':
            sys.stderr.write(u"[{}] will unfollow {}\n".format(action.action_id, action.action_tweet_text))
        # end if
        n_actions[action.action_type] += 1
        total_action += 1
    # end for

    # Type action
    for t in n_actions.keys():
        sys.stdout.write(u"{} action of type {} in the reservoir ({})\n".format(n_actions[t], t,
                                                                                u"full" if action_scheduler.full(
                                                                                    t) else u"not full"))
    # end for
# end list_actions
