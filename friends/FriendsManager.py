#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : FriendsManager.py
# Description : A class to manage followers and following in the database and the links
# between the DB and the Twitter manager class.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
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

import datetime
import executor
from patterns.singleton import singleton
import pyTweetBot
from sqlalchemy import update, delete
from sqlalchemy.orm import load_only
from sqlalchemy import and_, not_
import time
import logging
from datetime import timedelta
import tweepy


##############################################
# EXCEPTION
##############################################


# Exception, Useless action because already done (already following a user)
class ActionAlreadyDone(Exception):
    """
    Exception, useless action because already done (already following a user)
    """
    pass
# end ActionAlreadyDone


##############################################
# CLASS
##############################################


# The class manage followers and following in the database and do
# the links between the DB and the Twitter management part.
@singleton
class FriendsManager(object):
    """
    The class manage followers and following in the database and do
    the links between the DB and the Twitter management part.
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        # DB session
        self._session = pyTweetBot.db.DBConnector().get_session()

        # Twitter connection
        self._twitter_con = pyTweetBot.twitter.TweetBotConnector()

        # Logger
        self._logger = logging.getLogger(name=u"pyTweetBot")
    # end __init__

    ######################################################
    # PROPERTIES
    ######################################################

    # Get the number of followers
    @property
    def n_followers(self):
        """
        Get the nunber of followers.
        :return: The number of followers.
        """
        return pyTweetBot.twitter.TweetBotConnector().get_user().followers_count
    # end n_followers

    # Get the number of following
    @property
    def n_followings(self):
        """
        Get the number of following.
        :return: The number of following.
        """
        return pyTweetBot.twitter.TweetBotConnector().get_user().friends_count
    # end n_followers

    # Get followers cursor
    @property
    def followers_cursor(self):
        """
        Get followers cursor
        :return: Followers cursor
        """
        return tweepy.Cursor(self._api.followers)
    # end followers_cursor

    # Get followers
    @property
    def followers(self):
        """
        Get followers
        :return: A list of Friend objects
        """
        return self._session.query(db.obj.Friend).filter(db.obj.Friend.friend_follower).all()
    # end get_followers

    # Get following
    @property
    def followings(self):
        """
        Get following
        :return: A list of friend objects
        """
        return self._session.query(db.obj.Friend).filter(db.obj.Friend.friend_following).all()
    # end get_following

    ######################################################
    # PUBLIC FUNCTIONS
    ######################################################

    # Is friend a follower?
    def is_follower(self, screen_name):
        """
        Is friend a follower?
        :param screen_name: Friend's screen name
        :return: True or False
        """
        return self._session.query(db.obj.Friend).filter(and_(
            db.obj.Friend.friend_screen_name == screen_name, db.obj.Friend.friend_follower)).count > 0
    # end is_follower

    # Am I following this friend?
    def is_following(self, screen_name):
        """
        Am I following this friend?
        :param screen_name: Friend's screen name
        :return: True or False
        """
        return self._session.query(db.obj.Friend).filter(and_(db.obj.Friend.friend_screen_name == screen_name, db.obj.Friend.friend_following == 1)).count() > 0
    # end is_following

    # Get obsolete friends
    def get_obsolete_friends(self, days):
        """
        Get obsolete friends
        :param days: Number of days to be obsolete.
        :return: The list of obsolete friends.
        """
        # Transform back to date
        # Limit date
        datetime_limit = datetime.datetime.utcnow() - timedelta(days=days)

        # Get all
        return self._session.query(db.obj.Friend).filter(and_(db.obj.Friend.friend_following == True,
                                                  not_(db.obj.Friend.friend_follower == True),
                                                  db.obj.Friend.friend_following_date <= datetime_limit)).all()
    # end get_obsolete_friends

    # Get a friend from the DB
    def get_friend_by_id(self, friend_id):
        """
        Get a friend from the DB.
        :param friend_id: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(db.obj.Friend).filter(db.obj.Friend.friend_id == friend_id).one()
    # end get_friend_by_id

    # Get a friend from the DB
    def get_friend_by_name(self, screen_name):
        """
        Get a friend from the DB.
        :param screen_name: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(db.obj.Friend).filter(db.obj.Friend.friend_screen_name == screen_name).one()
    # end get_friend_by_name

    # Friend exists
    def exists(self, screen_name):
        """
        Check if we are followed by a Twitter account.
        :param screen_name: Account's screen name
        :return: True or False
        """
        return len(self._session.query(db.obj.Friend).filter(db.obj.Friend.friend_screen_name == screen_name).all()) > 0
    # end exists

    # Follow a Twitter account
    def follow(self, screen_name):
        """
        Follow a Twitter account
        :param screen_name: User's screen name
        :return: True if followed, False is already followed
        """
        # Follow if needed
        if not self.is_following(screen_name=screen_name):
            # Following on Twitter
            pyTweetBot.twitter.TweetBotConnector().follow(screen_name)

            # Get the Twitter user
            twf = pyTweetBot.twitter.TweetBotConnector().get_user(screen_name)

            # Add friend in the DB (if needed)
            self._add_friend(twf.screen_name, twf.description, twf.location, twf.followers_count,
                             twf.friends_count, twf.statuses_count)

            # Change DB
            self._set_following(screen_name, True)
        else:
            raise ActionAlreadyDone(u"Already following user {}".format(screen_name))
        # end if
    # end follow

    # Unfollow a Twitter account
    def unfollow(self, screen_name):
        """
        Unfollow a Twitter account
        :param screen_name: User's scree name
        :return: True of False if succeeded
        """
        # Unfollow if possible
        if self.is_following(screen_name=screen_name):
            # Unfollowing on Twitter
            pyTweetBot.twitter.TweetBotConnector().unfollow(screen_name)

            # Change DB
            self._set_following(screen_name, False)
        else:
            raise ActionAlreadyDone(u"Already not following user {}".format(screen_name))
        # end if
    # end unfollow

    # Update followers and following
    def update(self):
        """
        Update followers and following
        :return: New follower count, Lost follower count, New following count, Lost following count
        """
        # Update followers
        self._logger.info(u"Updating followers...")
        n_follower, d_follower = self._update_friends(self._twitter_con.get_followers_cursor(), follower=True)

        # Update following
        self._logger.info(u"Updating followings...")
        n_following, d_following = self._update_friends(self._twitter_con.get_following_cursor(), follower=False)

        # Insert a statistic
        self.update_statistics()

        return n_follower, d_follower, n_following, d_following
    # end update

    # Get followers cursor
    def get_followers_cursor(self):
        """
        Get followers cursor
        :return: Followers cursor
        """
        return tweepy.Cursor(self._api.followers)
    # end get_followers_cursor

    # Insert a value in the statistics table
    def update_statistics(self):
        """
        Insert a value in the statistics table.
        :return:
        """
        # New statistic object
        statistic = pyTweetBot.db.obj.Statistic(statistic_friends_count=self.n_following(),
                                     statistic_followers_count=self.n_followers(),
                                     statistic_statuses_count=executor.ActionScheduler().n_statuses())

        # Add the statistic
        self._session.add(statistic)

        # Commit changes
        self._session.commit()
        return self.n_followers, self.n_following, executor.ActionScheduler().n_statuses()
    # end _insert_statistic

    # Get followers
    def get_followers(self):
        """
        Get followers
        :return:
        """
        return self._session.query(pyTweetBot.db.obj.Friend).filter(pyTweetBot.db.obj.Friend.friend_follower).all()
    # end get_followers

    # Get following
    def get_following(self):
        """
        Get following
        :return:
        """
        return self._session.query(pyTweetBot.db.obj.Friend).filter(pyTweetBot.db.obj.Friend.friend_following).all()
    # end get_following

    ######################################################
    # PRIVATE FUNCTIONS
    ######################################################

    # Get last day follow/unfollow ratio
    def _follow_unfollow_ratio(self, action_type):
        """
        Get last day follow/unfollow ratio
        :return:
        """
        # Action type
        if action_type == 'follow':
            if self._unfollow_count == 0:
                return self._follow_count
            else:
                return float(self._follow_count) / float(self._unfollow_count)
            # end if
        else:
            if self._follow_count == 0:
                return self._unfollow_count
            else:
                return float(self._unfollow_count) / float(self._follow_count)
            # end if
        # end if
    # end _follow_unfollow_ratio

    # Increment follow counter
    def _inc_follow_counter(self):
        """
        Increment follow counter
        :return:
        """
        # Add to history
        self._follow_history.append(datetime.datetime.utcnow())

        # Last 24h list
        last_day_follows = list()
        last_day_counter = 0
        for follow_time in self._follow_history:
            if datetime.datetime.utcnow() - follow_time <= 60 * 60 * 24:
                last_day_follows.append(follow_time)
                last_day_counter += 1
            # end if
        # end for

        # History and counter
        self._follow_history = last_day_follows
        self._follow_count = last_day_counter
    # end _inc_follow_counter

    # Increment unfollow counter
    def _inc_unfollow_counter(self):
        """
        Increment unfollow counter
        :return:
        """
        self._unfollow_history.append(datetime.datetime.utcnow())

        # Last 24h list
        last_day_unfollows = list()
        last_day_counter = 0
        for unfollow_time in self._unfollow_history:
            if datetime.datetime.utcnow() - unfollow_time <= 60 * 60 * 24:
                last_day_unfollows.append(unfollow_time)
                last_day_counter += 1
                # end if
        # end for

        # History and counter
        self._unfollow_history = last_day_unfollows
        self._unfollow_count = last_day_counter
    # end _inc_unfollow_counter

    # Add a friend
    def _add_friend(self, screen_name, description, location, followers_count, friends_count,
                    statuses_count):
        """
        Add a friend in the MySQL database.
        :param screen_name: The Twitter account's screen name.
        :param description: The Twitter account's description.
        :param location: Twitter account's geographical location.
        :param followers_count: Twitter account's followers count.
        :param friends_count: Twitter account's friends count.
        :param statuses_count: Twitter account's statuses count.
        :return: 1 if a new friends created, 0 if updated only.
        """
        if not self.exists(screen_name):
            new_friend = pyTweetBot.db.obj.Friend(friend_screen_name=screen_name, friend_description=description,
                                       friend_location=location, friend_followers_count=followers_count,
                                       friend_friends_count=friends_count, friend_statuses_count=statuses_count)
            self._session.add(new_friend)
            self._logger.info(u"New friend %s" % screen_name)
            return 1
        else:
            update(pyTweetBot.db.obj.Friend).where(pyTweetBot.db.obj.Friend.friend_screen_name == screen_name).\
                values(friend_last_update=datetime.datetime.now())
            return 0
        # end if
    # end add_friend

    # Set this friend as follower
    def _set_follower(self, screen_name, follower=True):
        """
        Set this friend as follower.
        :param screen_name:
        :param follower:
        :return:
        """
        # Friend
        friend = self.get_friend_by_name(screen_name)

        # Log
        if follower and not friend.friend_follower:
            self._logger.info(u"New follower %s" % screen_name)
        elif friend.friend_follower and not follower:
            self._logger.info(u"Lost a follower %s" % screen_name)
        # end if

        # Counter and update
        if not friend.friend_follower and follower:
            count = 1
            friend.friend_follower = True
        elif friend.friend_follower and not follower:
            count = -1
            friend.friend_follower = False
        else:
            count = 0
        # end if

        # Update follower time if necessary
        if not follower:
            friend.friend_follower_date = None
        elif friend.friend_follower_date is None:
            friend.friend_follower_date = datetime.datetime.now()
        # end if

        return count
    # end _set_as_follower

    # Set this friend as following
    def _set_following(self, screen_name, following=True):
        """
        Set this friend as following.
        :param screen_name:
        :param following:
        :return: Counter of new following (-1 <= 0 <= 1)
        """
        # Friend
        friend = self.get_friend_by_name(screen_name)

        # Log
        if following and not friend.friend_following:
            self._logger.info(u"New following %s" % screen_name)
        elif not following and friend.friend_following:
            self._logger.info(u"Stopped following %s" % screen_name)
        # end if

        # Counter and change
        if not friend.friend_following and following:
            friend.friend_following = True
            count = 1
        elif friend.friend_following and not following:
            friend.friend_following = False
            count = -1
        else:
            count = 0
        # end if

        # Update follower time if necessary
        if not following:
            friend.friend_following_date = None
        elif friend.friend_following_date is None:
            friend.friend_following_date = datetime.datetime.now()
        # end if

        return count
    # end _set_as_follower

    # Update friends
    def _update_friends(self, cursor, follower=True):
        """
        Update friends
        :param cursor: Tweepy cursor
        :param follower: Update followers (True) or following (False)?
        :return: New entries counter, Deleted entries counter
        """
        # Get current friends.
        if follower:
            friends = self._session.query(pyTweetBot.db.obj.Friend).options(load_only('friend_screen_name')).filter(
                pyTweetBot.db.obj.Friend.friend_follower).all()
        else:
            friends = self._session.query(pyTweetBot.db.obj.Friend).options(load_only('friend_screen_name')).filter(
                pyTweetBot.db.obj.Friend.friend_following).all()
        # end if

        # Counter
        counter = 0
        deleted = 0

        # Get screen names
        last_friends = list()
        for friend in friends:
            last_friends.append(friend.friend_screen_name)
        # end for

        # For each page
        finished = False
        while not finished:
            try:
                for page in cursor.pages():
                    # For each friends
                    for twf in page:
                        # Add this friend if necessary
                        counter += self._add_friend(twf.screen_name, twf.description, twf.location, twf.followers_count,
                                                    twf.friends_count, twf.statuses_count)

                        # Update status type
                        if follower:
                            counter += self._set_follower(twf.screen_name)
                        else:
                            counter += self._set_following(twf.screen_name)

                        # Remove friend from list
                        try:
                            last_friends.remove(twf.screen_name)
                        except ValueError:
                            pass
                        # end try
                    # end for
                    # Commit and wait
                    self._session.commit()
                    time.sleep(60)
                # end for
                finished = True
            except tweepy.error.RateLimitError:
                # Rate limit reached, wait 5 minutes
                time.sleep(300)
                pass
            # end try
        # end while

        # Update status of friends not follower/following
        # anymore
        for name in last_friends:
            if follower:
                self._set_follower(screen_name=name, follower=False)
            else:
                self._set_following(screen_name=name, following=False)
            # end if
            deleted += 1
        # end for

        # Delete old friend
        self._clean_friendships()

        # Commit
        self._session.commit()

        return counter, deleted
    # end update_friends

    # Clean friendships
    def _clean_friendships(self):
        """
        Remove all friendships with no links
        :return:
        """
        # Select friend with no links
        no_links = self._session.query(pyTweetBot.db.obj.Friend).filter(not pyTweetBot.db.obj.Friend.friend_follower and not pyTweetBot.db.obj.Friend.friend_following).all()

        # Delete
        for no_link in no_links:
            delete(pyTweetBot.db.obj.Friend).where(pyTweetBot.db.obj.Friend.friend_screen_name == no_link.friend_screen_name)
        # end for
    # end _clean_friendship

# end FriendsManager
