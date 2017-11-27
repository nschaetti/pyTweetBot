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
import db
import db.obj
from twitter.TweetBotConnect import TweetBotConnector
from sqlalchemy import and_, or_
import logging
from patterns.singleton import singleton
import time
import tweepy
from threading import Thread
import random
import sys


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


# No factory set
class NoFactory(Exception):
    """
    No factory to create Tweets
    """
    pass
# end NoFactory


# Manage bot's action
@singleton
class ActionScheduler(Thread):
    """
    Manage bot's action
    """

    # Constructor
    def __init__(self, config, n_actions=None, update_delay=timedelta(minutes=10), reservoir_size=timedelta(days=3),
                 purge_delay=timedelta(weeks=2), stats=None):
        """
        Constructor
        :param config:
        :param n_actions:
        :param update_delay:
        :param reservoir_size:
        :param purge_delay:
        :param stats:
        """
        # Properties
        self._session = db.DBConnector().get_session()

        if n_actions == None:
            self._n_actions = {"FollowUnfollow": 1, "Like": 1, "Tweet": 1, "Retweet": 1}
        else:
            self._n_actions = n_actions
        # end if

        self._purge_delay = purge_delay
        self._reservoir_size = reservoir_size
        self._update_delay = update_delay
        self._config = config

        # Purge the reservoir
        self._purge_reservoir()

        # Tread
        Thread.__init__(self)

        # Stats
        self._stats_manager = stats
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

    # Add an action to the DB
    def add(self, action):
        """
        Add an action to the DB
        :param action:
        :return:
        """
        # Check that the reservoir is not full
        if not self.full(action.action_type):
            # Add action
            self._session.add(action)

            # Commit
            self._session.commit()
        else:
            raise ActionReservoirFullError(u"To many action in the reservoir to add a new one")
        # end if
    # end add

    # Add a follow action in the DB
    def add_follow(self, screen_name):
        """
        Add a "follow" action in the DB:
        :param friend_id:
        :return:
        """
        if not self.exists(action_type="FollowUnfollow", action_follow=screen_name):
            # Get empty actions
            empty_action = self._get_empty_follow_unfollow_action(type='follow')

            # Set empty action if exists
            if empty_action is not None:
                # Update
                empty_action.action_follow = screen_name
            else:
                # Insert
                new_action = db.obj.Action(action_type='FollowUnfollow', action_order=self._generate_random_order(),
                                           action_follow=screen_name)
                self._session.add(new_action)
            # end if
            self._session.commit()
        else:
            raise ActionAlreadyExists(
                u"Follow action for screen name {} already in database".format(screen_name))
        # end if
    # end add_follow

    # Add an unfollow action in the DB
    def add_unfollow(self, screen_name):
        """
        Add an "unfollow" action in the DB:
        :param friend_id: Twitter account0's ID.
        """
        if not self.exists(action_type="FollowUnfollow", action_unfollow=screen_name):
            # Get empty actions
            empty_action = self._get_empty_follow_unfollow_action(type='unfollow')

            # Set empty action if exists
            if empty_action is not None:
                # Update
                empty_action.action_unfollow = screen_name
            else:
                # Insert
                new_action = db.obj.Action(action_type='FollowUnfollow', action_order=self._generate_random_order(),
                                           action_unfollow=screen_name)
                self._session.add(new_action)
            # end if
            self._session.commit()
        else:
            raise ActionAlreadyExists(
                u"Unfollow action for screen name {} already in database".format(screen_name))
        # end if
    # end add_unfollow

    # Add a like action in the DB
    def add_like(self, tweet_id, tweet_text):
        """
        Add a "like" action in the DB.
        :param tweet_id: Tweet's ID.
        """
        self._add_action("Like", tweet_id, tweet_text)
    # end add_like

    # Add a tweet action in the DB
    def add_tweet(self, tweet):
        """
        Add a tweet action in the DB
        :param tweet: Text of the Tweet or Tweet object.
        """
        if type(tweet) is unicode or type(tweet) is str:
            self._add_text_action("Tweet", tweet)
        else:
            self._add_text_action("Tweet", tweet.get_tweet())
        # end if
    # end add_tweet

    # Add a "Retweet" action in the DB
    def add_retweet(self, tweet_id, tweet_text):
        """
        Add a "retweet" action in the DB
        :param tweet_id: Tweet's ID
        """
        self._add_action("Retweet", tweet_id, tweet_text)
    # end add_retweet

    # Does an action already exists in the DB?
    def exists(self, action_type, action_tweet_id=None, action_tweet_text=None, action_follow=None, action_unfollow=None):
        """
        Does an action already exists in the DB?
        :param action_type: Type of action
        :param action_tweet_id: Tweet's ID (can be None)
        :param action_tweet_text: Tweet's text (can be None)
        :return: True or False
        """
        try:
            if action_type == 'FollowUnfollow' and action_follow is not None and action_unfollow is None:
                self._session.query(db.obj.Action).filter(
                    and_(
                        db.obj.Action.action_type == action_type,
                        db.obj.Action.action_follow == action_follow
                    )
                ).one()
                return True
            elif action_type == 'FollowUnfollow' and action_follow is None and action_unfollow is not None:
                self._session.query(db.obj.Action).filter(
                    and_(
                        db.obj.Action.action_type == action_type,
                        db.obj.Action.action_unfollow == action_unfollow
                    )
                ).one()
                return True
            elif action_tweet_id is None and action_tweet_text is None:
                self._session.query(db.obj.Action).filter(db.obj.Action.action_type == action_type).one()
                return True
            elif action_tweet_id is not None and action_tweet_text is None:
                self._session.query(db.obj.Action).filter(
                    and_(db.obj.Action.action_type == action_type, db.obj.Action.action_tweet_id == action_tweet_id)).one()
                return True
            elif action_tweet_id is None and action_tweet_text is not None:
                self._session.query(db.obj.Action).filter(
                    and_(db.obj.Action.action_type == action_type, db.obj.Action.action_tweet_text == action_tweet_text)).one()
                return True
            else:
                self._session.query(db.obj.Action).filter(
                    and_(db.obj.Action.action_type == action_type, db.obj.Action.action_tweet_id == action_tweet_id,
                         db.obj.Action.action_tweet_text == action_tweet_text)).one()
                return True
            # end if
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try
    # end exists

    # Delete an action
    def delete(self, action):
        """
        Delete an action
        :param action: Action to delete.
        """
        self._session.query(db.obj.Action).filter(db.obj.Action.action_id == action.action_id).delete()
        self._session.commit()
    # end delete

    # Execute next actions
    def exec_next_actions(self):
        """
        Execute next actions
        :return:
        """
        for action_type in ["FollowUnfollow", "Like", "Tweet", "Retweet"]:
            # Get action to be executed
            self.exec_next_action(action_type=action_type)
        # end for
    # end exec_next_action

    # Execute next action (by type)
    def exec_next_action(self, action_type):
        """
        Execute next action (by type)
        :param action_type: Action's type (like, follow, etc)
        :return:
        """
        # Get all actions
        action = self._session.query(db.obj.Action).filter(db.obj.Action.action_type == action_type) \
            .order_by(db.obj.Action.action_id).all()[0]
        action.execute()
        self.delete(action)
    # end exec_next_action

    # List actions in the reservoir
    def list_actions(self, action_type=""):
        """
        List actions in the reservoir
        :return:
        """
        # Get actions
        if action_type == "":
            return self._session.query(db.obj.Action).order_by(db.obj.Action.action_id).all()
        else:
            return self._session.query(db.obj.Action).filter(db.obj.Action.action_type == action_type).order_by(db.obj.Action.action_id).all()
        # end if
    # end list_actions

    # Is reservoir empty
    def empty(self, action_type):
        """
        Is the reservoir empty?
        :param action_type: Action type
        :return: True or False
        """
        return self._get_reservoir_level(action_type) == 0
    # end if

    # Check if the actions reservoir is full.
    def full(self, action_type):
        """
        Check if the actions reservoir is full for this
        kind of action.
        :param action_type: The kind of action
        :return:
        """
        # Get reservoir level
        reservoir_level = self._get_reservoir_level(action_type)

        # Max number of actions
        max_n_action = int(self._reservoir_size.total_seconds() / self._update_delay.total_seconds()
                           * self._n_actions[action_type])

        # Log
        logging.debug(u"is_reservoir_full: {} in the reservoir for a max value of {}".format(reservoir_level,
                                                                                            max_n_action))

        # reservoir_level >= max_n_action => full
        return reservoir_level >= max_n_action
    # end _is_reservoir_full

    # Get the number of statuses
    def n_statuses(self):
        """
        Get the number of statuses
        :return: The number of statuses
        """
        return TweetBotConnector().get_user().statuses_count
    # end n_statuses

    ##############################################
    # Private functions
    ##############################################

    # Generate random order
    def _generate_random_order(self):
        """
        Generate random order
        :return:
        """
        return random.randint(0, sys.maxint)
    # end _generate_random_order

    # Get empty follow-unfollow action
    def _get_empty_follow_unfollow_action(self, type):
        """
        Get an empty follow-unfollow action
        :param type: Action type (follow, unfollow)
        :return:
        """
        if type == 'follow':
            empty_actions = self._session\
            .query(db.obj.Action)\
            .filter(
                and_(
                    db.obj.Action.action_type == "FollowUnfollow",
                    db.obj.Action.action_follow == None,
                    db.obj.Action.action_unfollow != None
                )
            ).all()
        else:
            empty_actions = self._session \
                .query(db.obj.Action) \
                .filter(
                and_(
                    db.obj.Action.action_type == "FollowUnfollow",
                    db.obj.Action.action_follow != None,
                    db.obj.Action.action_unfollow == None
                )
            ).all()
        # end if

        # Results
        if len(empty_actions) > 0:
            return empty_actions[0]
        else:
            return None
        # end if
    # end _get_empty_follow_unfollow_action

    # Purge reservoir
    def _purge_reservoir(self):
        """
        Purge the reservoir of obsolete actions.
        """
        self._session.query(db.obj.Action).filter(db.obj.Action.action_date <= datetime.datetime.utcnow() - self._purge_delay)
    # end _purge_reservoir

    # Get reservoir levels
    def _get_reservoir_levels(self):
        """
        Get the number of actions in the reservoir.
        :return: The number of action as a dict()
        """
        result = dict()
        # Level per action
        for action_type in ["FollowUnfollow", "Like", "Tweet", "Retweet"]:
            result[action_type] = self._get_reservoir_level(action_type)
        # end for
        return result
    # end _get_reservoir_level

    # Get reservoir level
    def _get_reservoir_level(self, action_type):
        """
        Get the number of action for a action type.
        :param action_type: Action's type.
        :return: Reservoir level for this action
        """
        return len(self._session.query(db.obj.Action).filter(db.obj.Action.action_type == action_type).all())
    # end _get_reservoir_level

    # Get action to execute
    def _get_exec_action(self, action_type):
        """
        Get all action to execute
        :return: Action to execute as a list()
        """
        # Get all actions
        if action_type == 'FollowUnfollow':
            exec_actions = self._session.query(db.obj.Action)\
                .filter(
                    and_(
                        db.obj.Action.action_type == action_type,
                        db.obj.Action.action_follow != None,
                        db.obj.Action.action_unfollow != None
                    )
                )\
                .order_by(db.obj.Action.action_order).all()
        else:
            exec_actions = self._session.query(db.obj.Action).filter(db.obj.Action.action_type == action_type)\
                .order_by(db.obj.Action.action_order).all()
        # end if
        return exec_actions[:self._n_actions[action_type]]
    # end _get_exec_action

    # Add action with id
    def _add_id_action(self, action_type, the_id):
        """
        Add action with a id argument.
        :param action_type: Type of action
        :param the_id: Action's ID
        """
        if not self.exists(action_type, the_id):
            action = db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_id=the_id)
            self.add(action)
        else:
            logging.getLogger(u"pyTweetBot").warning(u"{} action for friend/tweet {} already in database"
                                                    .format(action_type, the_id))
            raise ActionAlreadyExists(u"{} action for friend/tweet {} already in database".format(action_type, the_id))
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
            action = db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_text=the_text)
            self.add(action)
        else:
            logging.getLogger(u"pyTweetBot").warning(u"{} action for text {} already in database"
                                                    .format(action_type, the_text))
            raise ActionAlreadyExists(u"{} action for text {} already in database".format(action_type, the_text))
        # end if
    # end _add_text_action

    # Add action with text and ID
    def _add_action(self, action_type, the_id, the_text):
        """
        Add action with text and ID
        :param action_type:
        :param the_id:
        :param the_text:
        :return:
        """
        if not self.exists(action_type=action_type, action_tweet_id=the_id, action_tweet_text=the_text):
            action = db.obj.Action(action_type=action_type, action_order=self._generate_random_order(),
                                   action_tweet_id=the_id, action_tweet_text=the_text)
            self.add(action)
        else:
            logging.getLogger(u"pyTweetBot").warning(u"{} action for id {} and text {} already in database"
                                                     .format(action_type, the_id, the_text))
            raise ActionAlreadyExists(
                u"{} action for id {} and text {} already in database".format(action_type, the_id, the_text))
        # end if
    # end _add_action

    ##############################################
    # Override functions
    ##############################################

    # Execute
    def __call__(self):
        """
        Execute action
        :return:
        """
        # Action to execute
        action_to_execute = list()
        n_action = 0

        # Level per action
        for action_type in ["FollowUnfollow", "Like", "Tweet", "Retweet"]:
            # Get actions to be executed
            for action in self._get_exec_action(action_type):
                # Add to list of action to execute
                action_to_execute.append(action)
                n_action += 1
            # end for
        # end for

        # For each action to execute
        for i in range(n_action):
            # Choose an action randomly
            action = random.choice(action_to_execute)

            # Try to execute
            try:
                # Delete action
                self.delete(action)
                action_to_execute.remove(action)

                # Execute
                action.execute()

                # Wait
                self._config.wait_next_action()
            except tweepy.TweepError as e:
                logging.getLogger(u"pyTweetBot").error(
                    u"Error while executing action {} : {}".format(action, e))
            # end try
        # end for
    # end __call__

# end ActionScheduler
