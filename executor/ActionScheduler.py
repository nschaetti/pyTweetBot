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
from sqlalchemy import or_, and_, not_


# Reservoir full exception
class ActionReservoirFullError(Exception):
    """
    Reservoir is full
    """
    pass
# end ActionReservoirFullError

# Action already in the DB
class ActionAlreadyExists(Exception):
    """
    The action is already registered in the DB
    """
    pass
# end ActionAlreadyExists


# Manage bot's action
class ActionScheduler(object):

    # Constructor
    def __init__(self):
        # Properties
        self._session = DBConnector().get_session()

        # Get last information
        self._last_actions_date = self._get_last_date()

        # Action delay
        self._action_delays = {'Follow': 10, 'Unfollow' : 10, 'Tweet' : 10, 'Retweet': 10, 'Like': 10}
    # end __init__

    ##############################################
    #
    # Public functions
    #
    ##############################################

    # Add an action to the DB
    def add(self, action):
        """
        Add an action to the DB
        :param action:
        :return:
        """
        # Check that the reservoir is not full
        if not self._is_reservoir_full(action.action_type):
            # Check if action already exists
            # Change date
            action.action_exec_date = self._get_next_available_date(action.action_type)
            self._last_actions_date[action.action_type] = action.action_exec_date

            # Add action
            self._session.add(action)

            # Commit
            self._session.commit()
        else:
            raise ActionReservoirFullError("To many action in the reservoir to add a new one")
        # end if
    # end add

    # Add a follow action in the DB
    def add_follow(self, friend_id):
        """
        Add a "follow" action in the DB:
        :param friend_id:
        :return:
        """
        self._add_id_action("Follow", friend_id)
    # end add_follow

    # Add an unfollow action in the DB
    def add_unfollow(self, friend_id):
        """
        Add an "unfollow" action in the DB:
        :param friend_id: Twitter account0's ID.
        """
        self._add_id_action("Unfollow", friend_id)
    # end add_unfollow

    # Add a like action in the DB
    def add_like(self, tweet_id):
        """
        Add a "like" action in the DB.
        :param tweet_id: Tweet's ID.
        """
        self._add_id_action("Like", tweet_id)
    # end add_like

    # Add a tweet action in the DB
    def add_tweet(self, tweet_text):
        """
        Add a tweet actio in the DB
        :param tweet_text: Text of the Tweet
        """
        pass
    # end add_tweet

    # Add a "Retweet" action in the DB
    def add_retweet(self, tweet_id):
        """
        Add a "retweet" action in the DB
        :param tweet_id: Tweet's ID
        """
        self._add_id_action("Retweet", tweet_id)
    # end add_retweet

    # Does an action already exists in the DB?
    def exists(self, action_type, action_tweet_id=None, action_tweet_text=None):
        """
        Does an action already exists in the DB?
        :param action_type: Type of action
        :param action_tweet_id: Tweet's ID (can be None)
        :param action_tweet_text: Tweet's text (can be None)
        :return: True or False
        """
        try:
            if action_tweet_id is None and action_tweet_text is None:
                self._session.query(Action).filter(Action.action_type == action_type).one()
                return True
            elif action_tweet_id is not None and action_tweet_text is None:
                self._session.query(Action).filter(
                    and_(Action.action_type == action_type, Action.action_tweet_id == action_tweet_id)).one()
                return True
            elif action_tweet_id is None and action_tweet_text is not None:
                self._session.query(Action).filter(
                    and_(Action.action_type == action_type, Action.action_tweet_text == action_tweet_text)).one()
                return True
            else:
                self._session.query(Action).filter(
                    and_(Action.action_type == action_type, Action.action_tweet_id == action_tweet_id,
                         Action.action_tweet_text == action_tweet_text)).one()
                return True
            # end if
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    ##############################################
    #
    # Private functions
    #
    ##############################################

    # Add action with id
    def _add_id_action(self, action_type, the_id):
        """
        Add action with id
        :param action_type: Type of action
        :param the_id: Action's ID
        """
        if not self.exists(action_type, the_id):
            action = Action(action_type=action_type, action_tweet_id=the_id)
            self.add(action)
        else:
            raise ActionAlreadyExists("{} action for friend/tweet {} already in database".format(action_type, the_id))
        # end if
    # end _add_id_action

    # Add action with text
    def _add_text_action(self, action_type, the_text):
        """
        Add action with text.
        :param action_type: Type of action
        :param the_text: Action's text.
        """
        if not self.exists(action_type=action_type, action_tweet_text=the_text):
            action = Action(action_tweet_text=the_text)
            self.add(action)
        else:
            raise ActionAlreadyExists("{} action for text {} already in database".format(action_type, the_text))
        # end if
    # end _add_text_action

    # Get next available date
    def _get_next_available_date(self, action_type):
        """
        Get the next available date for an action type.
        :param action_type: The kind of action.
        :return: Next available date
        """
        return self._last_actions_date[action_type] + timedelta(minutes=self._action_delays[action_type])
    # end _get_next_available_date

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
    def _get_default_last_action_date(self, action_type):
        """
        Return default last action date
        :param action:
        :return:
        """
        # Try to get the date
        try:
            last_action = self._session.query(Action).filter(Action.action_type == action_type)\
                    .order_by(desc(Action.action_exec_date)).one()
        except sqlalchemy.orm.exc.NoResultFound:
            # Do not exists
            return datetime.datetime.utcnow()
        # end try

        return last_action.action_exec_date
    # end _get_default_last_action_date

    # Get the date of the last actions
    def _get_last_date(self):
        """
        Get the date of the last actions in the DB
        :return:
        """
        # Last actions date
        last_follow_date = self._get_default_last_action_date('Follow')
        last_unfollow_date = self._get_default_last_action_date('Unfollow')
        last_tweet_date = self._get_default_last_action_date('Tweet')
        last_retweet_date = self._get_default_last_action_date('Retweet')
        last_like_date = self._get_default_last_action_date('Like')

        # Return
        return {'Follow': last_follow_date, 'Unfollow': last_unfollow_date, 'Tweet': last_tweet_date,
                'Retweet' : last_retweet_date, 'Like': last_like_date}
    # end _get_last_date

# end ActionScheduler
