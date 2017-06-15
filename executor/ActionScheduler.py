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

import sqlalchemy
import datetime
from datetime import timedelta
from db.obj.Action import Action
from db.DBConnector import DBConnector
from sqlalchemy import desc


# Manage bot's action
class ActionScheduler(object):

    # Constructor
    def __init__(self):
        # Properties
        self._session = DBConnector().get_session()

        # Get last information
        self._last_actions_date = self._get_last_date()
    # end __init__

    ##############################################
    #
    # Public functions
    #
    ##############################################

    # Add an action to the DB
    def add(self, action):
        # Check that the reservoir is not full
        if not self._is_reservoir_full(action.action_type):
            pass
            # Add action
        # end if
        return False
    # end add

    ##############################################
    #
    # Private functions
    #
    ##############################################

    # Check if the actions reservoir is full.
    def _is_reservoir_full(self, action_type):
        """
        Check if the actions reservoir is full for this
        kind of action.
        :param action_type: The kind of action
        :return:
        """
        # Last date
        last_date = self._last_actions_date[action_type]

        # Current time + delay
        delay = datetime.datetime.utcnow() + timedelta(days=3)

        # Last date > (now + 3days) => full
        return last_date > delay
    # end _is_reservoir_full

    # Return default last action date
    def _get_default_last_action_date(self, action):
        """
        Return default last action date
        :param action:
        :return:
        """
        return action.action_exec_date if action is not None else datetime.datetime.utcnow()
    # end _get_default_last_action_date

    # Get the date of the last actions
    def _get_last_date(self):
        """
        Get the date of the last actions in the DB
        :return:
        """
        # Last actions
        last_follow_action = self._session.query(Action).filter(Action.action_type == 'Follow')\
            .order_by(desc(Action.action_exec_date)).one()
        last_unfollow_action = self._session.query(Action).filter(Action.action_type == 'Unfollow')\
            .order_by(desc(Action.action_exec_date)).one()
        last_tweet_action = self._session.query(Action).filter(Action.action_type == 'Tweet')\
            .order_by(desc(Action.action_exec_date)).one()
        last_retweet_action = self._session.query(Action).filter(Action.action_type == 'Retweet')\
            .order_by(desc(Action.action_exec_date)).one()

        # Last actions date
        last_follow_date = self._get_default_last_action_date(last_follow_action)
        last_unfollow_date = self._get_default_last_action_date(last_unfollow_action)
        last_tweet_date = self._get_default_last_action_date(last_tweet_action)
        last_retweet_date = self._get_default_last_action_date(last_retweet_action)

        # Return
        return {'Follow': last_follow_date, 'Unfollow': last_unfollow_date, 'Tweet': last_tweet_date,
                'Retweet' : last_retweet_date}
    # end _get_last_date

# end ActionScheduler
