#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import datetime
from db.DBConnector import DBConnector
from db.obj.Friend import Friend
from db.obj.Follower import Follower
from db.obj.Following import Following
from patterns.singleton import singleton
from twitter.TweetBotConnect import TweetBotConnector
from sqlalchemy import update, delete, select
from sqlalchemy.orm import load_only
import sqlalchemy.orm.exc
import time


@singleton
class FriendsManager(object):

    # Constructor
    def __init__(self):
        # DB session
        self._session = DBConnector().get_session()

        # Twitter connection
        self._twitter_con = TweetBotConnector()
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
        :param screen_name:
        :return:
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name and Friend.friend_follower)) > 0
    # end is_follower

    # Am I following this friend?
    def is_following(self, screen_name):
        """
        Am I following this friend?
        :param screen_name:
        :return:
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name and Friend.friend_following)) > 0
    # end is_following

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
        Follower exists.
        :param screen_name:
        :return:
        """
        return len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name).all()) > 0
    # end exists

    # Update followers and following
    def update(self):
        """
        Update followers and following
        :return:
        """
        # Time of the update
        update_time = datetime.datetime.now()

        # Update followers
        new_follower_count = self._update_friends(self._twitter_con.get_followers_cursor(), follower=True)

        # Update following
        new_following_count = self._update_friends(self._twitter_con.get_following_cursor(), follower=False)

        return new_follower_count, new_following_count
    # end update

    ######################################################
    #
    # PRIVATE FUNCTIONS
    #
    ######################################################

    # Add a friend
    def _add_friend(self, screen_name, description, location, followers_count, friends_count,
                    statuses_count):
        """
        Add a friend in the DB
        :param screen_name:
        :param description:
        :param location:
        :param followers_count:
        :param friends_count:
        :param statuses_count:
        :return:
        """
        if not self.exists(screen_name):
            new_friend = Friend(friend_screen_name=screen_name, friend_description=description,
                                friend_location=location, friend_followers_count=followers_count,
                                friend_friends_count=friends_count, friend_statuses_count=statuses_count)
            self._session.add(new_friend)
        else:
            update(Friend).where(Friend.friend_screen_name == screen_name).\
                values(friend_last_update=datetime.datetime.now())
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

        # Update
        update(Friend).where(Friend.friend_screen_name == screen_name).values(friend_follower=follower)

        # Update follower time if necessary
        if not follower:
            update(Friend).where(Friend.friend_screen_name == screen_name).values(friend_follower_date=None)
        elif friend.friend_follower_date is None:
            update(Friend).where(Friend.friend_screen_name == screen_name).values(friend_follower_date=datetime.datetime.now())
        # end if
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

        # Update
        update(Friend).where(Friend.friend_screen_name == screen_name).values(friend_following=following)

        # Update follower time if necessary
        if not following:
            update(Friend).where(Friend.friend_screen_name == screen_name).values(friend_following_date=None)
        elif friend.friend_follower_date is None:
            update(Friend).where(Friend.friend_screen_name == screen_name).values(
                friend_following_date=datetime.datetime.now())
        # end if
    # end _set_as_follower

    # Update friends
    def _update_friends(self, cursor, follower=True):
        """
        Update friends
        :param cursor: Tweepy cursor.
        :param follower: Update followers?
        :return: Number of new entries
        """
        # Add count
        add_count = 0

        # Get current friends
        if follower:
            #friends = select(['friend_screen_name']).where(Friend.friend_follower)
            friends = self._session.query(Friend).options(load_only('friend_screen_name'))\
                .filter(Friend.friend_follower).all()
        else:
            #friends = select(['friend_sceeen_name']).where(Friend.friend_following)
            friends = self._session.query(Friend).options(load_only('friend_screen_name'))\
                .filter(Friend.friend_following).all()
        # end if
        print(friends)
        for friend in friends:
            print(friend)
        # end for
        exit()

        # For each page
        for page in cursor:
            # For each follower
            for twf in page:
                # Add this friend if necessary
                self._add_friend(twf.screen_name, twf.description, twf.location, twf.followers_count,
                                 twf.friends_count, twf.statuses_count)
                # Update status type
                if follower:
                    self._set_follower(twf.screen_name)
                else:
                    self._set_following(twf.screen_name)
            # end for
            # Commit and wait
            self._session.commit()
            time.sleep(60)
        # end for

        return add_count
    # end update_friends

# end FriendsManager
