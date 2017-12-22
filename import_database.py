#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : import_database.py
# Description : Import database.
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

import db.obj
from sqlalchemy import and_, or_
import os
import pickle
import logging
import tools.strings as pystr


# Import actions
def import_actions(session, actions):
    """
    Import actions
    :param session:
    :param actions:
    :return:
    """
    # For each action
    for action in actions:
        # Type
        if session.query(db.obj.Action).filter(
                and_(db.obj.Action.action_type == action.action_type,
                     db.obj.Action.action_id == action.action_id,
                     db.obj.Action.action_tweet_text == action.action_tweet_text)).count() > 0:
            logging.getLogger(pystr.LOGGER).error(u"Action {} already exists".format(action))
        else:
            # Add
            session.add(action)

            # Commit
            session.commit()

            # Log
            logging.getLogger(pystr.LOGGER).info(u"Action {} added".format(action))
        # end if
    # end for
# end import actions


# Import friends
def import_friends(session, friends):
    """
    Import friends
    :param session:
    :param friends:
    :return:
    """
    # For each friend
    for friend in friends:
        # Exists?
        if session.query(db.obj.Friend).filter(and_(db.obj.Friend.friend_screen_name == friend.friend_screen_name)):
            logging.getLogger(pystr.LOGGER).error(u"Friend {} already exists".format(friend))
        else:
            # Add
            session.add(friend)

            # Commit
            session.commit()

            # Log
            logging.getLogger(pystr.LOGGER).info(u"Friend {} added".format(friend))
        # end if
    # end for
# end import_friends


# Import statistics
def import_statistics(session, statistics):
    """
    Import statistics
    :param session:
    :param statistics:
    :return:
    """
    # For each statistics
    for statistic in statistics:
        # Exists?
        if session.query(db.obj.Statistic).filter(and_(db.obj.Statistic.statistic_date)):
            logging.getLogger(pystr.LOGGER).error(u"Statistic {} already exists".format(statistic))
        else:
            # Add
            session.add(statistic)

            # Commit
            session.commit()

            # Log
            logging.getLogger(pystr.LOGGER).info(u"Statistic {} added".format(statistic))
        # end if
    # end for
# end import_statistics


# Import tweeted
def import_tweets(session, tweets):
    """
    Import tweets
    :param session:
    :param tweets:
    :return:
    """
    # For each tweets
    for tweet in tweets:
        # Exists?
        if session.query(db.obj.Tweeted).filter(or_(db.obj.Tweeted.tweet_tweet_text == tweet.tweet_tweet_text,
                                                    db.obj.Tweeted.tweet_tweet_id == tweet.tweet_tweet_id)).count() > 0:
            logging.getLogger(pystr.LOGGER).error(u"Tweeted {} already exists".format(tweet))
        else:
            # Add
            session.add(tweet)

            # Commit
            session.commit()

            # Log
            logging.getLogger(pystr.LOGGER).info(u"Tweeted {} added".format(tweet))
        # end if
    # end for
# end import_tweets


# Function to import the database
def import_database(output_dir, mysql_connector):
    """
    Function to import the database
    :param output_dir:
    :param mysql_connector:
    :return:
    """
    # DB session
    mysql_session = mysql_connector.get_session()

    # Files
    actions_file = os.path.join(output_dir, u"actions.p")
    friends_file = os.path.join(output_dir, u"friends.p")
    statistics_file = os.path.join(output_dir, u"statistics.p")
    tweets_file = os.path.join(output_dir, u"tweets.p")

    # Load files
    actions = pickle.load(open(actions_file, 'rb'))
    friends = pickle.load(open(friends_file, 'rb'))
    statistics = pickle.load(open(statistics_file, 'rb'))
    tweets = pickle.load(open(tweets_file, 'rb'))

    # Import actions
    logging.getLogger(pystr.LOGGER).info(u"Importing actions...")
    import_actions(mysql_session, actions)

    # Import friends
    logging.getLogger(pystr.LOGGER).info(u"Importing friends...")
    import_friends(mysql_session, friends)

    # Import statistics
    logging.getLogger(pystr.LOGGER).info(u"Importing statistics...")
    import_statistics(mysql_session, statistics)

    # Import tweets
    logging.getLogger(pystr.LOGGER).info(u"Importing tweets...")
    import_tweets(mysql_session, tweets)
# end export_database
