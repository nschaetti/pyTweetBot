#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import datetime
from db.DBConnector import DBConnector
from executor.ActionScheduler import ActionScheduler
from db.obj.Friend import Friend
from db.obj.Statistic import Statistic
from patterns.singleton import singleton
from twitter.TweetBotConnect import TweetBotConnector
from sqlalchemy import update, delete, select
from sqlalchemy.orm import load_only
from sqlalchemy import or_, and_, not_
import time
import logging
from datetime import timedelta
import tweepy


@singleton
class FriendsManager(object):
    """
    Class to manager friendships
    """

    # Constructor
    def __init__(self):
        """
        Constructor
        """
        # DB session
        self._session = DBConnector().get_session()

        # Twitter connection
        self._twitter_con = TweetBotConnector()

        # Logger
        self._logger = logging.getLogger(name="pyTweetBot")
    # end __init__

    ######################################################
    #
    # PUBLIC FUNCTIONS
    #
    ######################################################

    # Is friend a follower?
    def is_follower(self, screen_name):
        """
        Is friend a follower?
        :param screen_name: Friend's screen name
        :return: True or False
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name and Friend.friend_follower)) > 0
    # end is_follower

    # Am I following this friend?
    def is_following(self, screen_name):
        """
        Am I following this friend?
        :param screen_name: Friend's screen name
        :return: True or False
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name and Friend.friend_following)) > 0
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
        return self._session.query(Friend).filter(and_(Friend.friend_following == True,
                                                  not_(Friend.friend_follower == True),
                                                  Friend.friend_following_date <= datetime_limit)).all()
    # end get_obsolete_friends

    # Get a friend from the DB
    def get_friend_by_id(self, friend_id):
        """
        Get a friend from the DB.
        :param friend_id: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(Friend).filter(Friend.friend_id == friend_id).one()
    # end get_friend_by_id

    # Get a friend from the DB
    def get_friend_by_name(self, screen_name):
        """
        Get a friend from the DB.
        :param screen_name: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        return self._session.query(Friend).filter(Friend.friend_screen_name == screen_name).one()
    # end get_friend_by_name

    # Friend exists
    def exists(self, screen_name):
        """
        Check if we are followed by a Twitter account.
        :param screen_name: Account's screen name
        :return: True or False
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name).all()) > 0
    # end exists

    # Follow a Twitter account
    def follow(self, screen_name):
        """
        Follow a Twitter account
        :param screen_name: User's screen name
        :return: True or False if succeeded
        """
        pass
    # end follow

    # Unfollow a Twitter account
    def unfollow(self, screen_name):
        """
        Unfollow a Twitter account
        :param screen_name: User's scree name
        :return: True of False if succeeded
        """
        pass
    # end unfollow

    # Update followers and following
    def update(self):
        """
        Update followers and following
        :return: New follower count, Lost follower count, New following count, Lost following count
        """
        # Update followers
        self._logger.info("Updating followers...")
        n_follower, d_follower = self._update_friends(self._twitter_con.get_followers_cursor(), follower=True)

        # Update following
        self._logger.info("Updating followings...")
        n_following, d_following = self._update_friends(self._twitter_con.get_following_cursor(), follower=False)

        # Insert a statistic
        self.insert_statistic()

        return n_follower, d_follower, n_following, d_following
    # end update

    # Get the number of followers
    def n_followers(self):
        """
        Get the nunber of followers.
        :return: The number of followers.
        """
        return self._session.query(Friend).filter(Friend.friend_follower == True).count()
    # end n_followers

    # Get the number of following
    def n_following(self):
        """
        Get the nunber of following.
        :return: The number of following.
        """
        return self._session.query(Friend).filter(Friend.friend_following == True).count()
    # end n_followers

    ######################################################
    #
    # PRIVATE FUNCTIONS
    #
    ######################################################

    # Insert a value in the statistics table
    def insert_statistic(self):
        """
        Insert a value in the statistics table.
        """
        statistic = Statistic(statistic_friends_count=self.n_following(), statistic_followers_count=self.n_followers(),
                              statistic_statuses_count=ActionScheduler().n_statuses())
        self._session.add(statistic)
        self._session.commit()
    # end _insert_statistic

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
            new_friend = Friend(friend_screen_name=screen_name, friend_description=description,
                                friend_location=location, friend_followers_count=followers_count,
                                friend_friends_count=friends_count, friend_statuses_count=statuses_count)
            self._session.add(new_friend)
            self._logger.info("New friend %s" % screen_name)
            return 1
        else:
            update(Friend).where(Friend.friend_screen_name == screen_name).\
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
            self._logger.info("New follower %s" % screen_name)
        # end if

        # Counter and update
        if not friend.friend_follower and follower:
            count = 1
            friend.friend_follower = follower
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
        :return:
        """
        # Friend
        friend = self.get_friend_by_name(screen_name)

        # Counter and change
        if not friend.friend_following and following:
            count = 1
        else:
            count = 0
        # end if

        # Log
        if following and not friend.friend_following:
            self._logger.info("New following %s" % screen_name)
        # end if

        # Update

        # Counter and change
        if not friend.friend_following and following:
            friend.friend_following = following
            count = 1
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
        :param cursor: Tweepy cursor.
        :param follower: Update followers?
        :return: Number of new entries
        """
        # Get current friends.
        if follower:
            friends = self._session.query(Friend).options(load_only('friend_screen_name')).filter(Friend.friend_follower).all()
        else:
            friends = self._session.query(Friend).options(load_only('friend_screen_name')).filter(Friend.friend_following).all()
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
                for page in cursor:
                    # For each follower
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
        no_links = self._session.query(Friend).filter(not Friend.friend_follower and not Friend.friend_following).all()

        # Delete
        for no_link in no_links:
            delete(Friend).where(Friend.friend_screen_name == no_link.friend_screen_name)
        # end for
    # end _clean_friendship

# end FriendsManager
