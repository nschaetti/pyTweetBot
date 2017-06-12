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
from sqlalchemy import update, delete
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
    # end __init_-

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

    # Get a follower from the DB
    def get_follower(self, screen_name):
        """
        Get a follower from the DB.
        :param screen_name: Follower's screen name.
        :return:
        """
        return self._session.query(Follower).filter(Follower.follower_friend.screen_name == screen_name).one()
    # end get_follower

    # Friend exists
    def exists(self, screen_name):
        """
        Follower exists.
        :param screen_name:
        :return:
        """
        if len(self._session.query(Friend).filter(Friend.friend_screen_name == screen_name).all()) > 0:
            return True
        # end if
        return False
    # end exists

    # Follower exists
    def follower_exists(self, screen_name):
        """
        The follower exists in the DB.
        :param screen_name:
        :return:
        """
        # Friend
        try:
            friend = self.get_friend_by_name(screen_name)
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try

        # If link exists
        if len(self._session.query(Follower).filter(Follower.follower_friend == friend.friend_id).all()) > 0:
            return True
        # end if
        return False
    # end follower_exists

    # Following exists
    def following_exists(self, screen_name):
        """
        The following exists
        :param screen_name:
        :return:
        """
        # Friend
        try:
            friend = self.get_friend_by_name(screen_name)
        except sqlalchemy.orm.exc.NoResultFound:
            return False
        # end try

        # If link exists
        if len(self._session.query(Following, Friend).filter(Following.following_friend == friend.friend_id).all()) > 0:
            return True
        # end if
        return False
    # end following_exists

    # Add a friend
    def add_friend(self, screen_name, description, location, followers_count, friends_count, statuses_count):
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
            return new_friend
        else:
            return self.get_friend_by_name(screen_name)
        # end if
    # end add_friend

    # Add a follower
    def add_follower(self, follower, update_time=datetime.datetime.now()):
        """
        Add follower
        :param follower: Twitter follower
        :param update_time: Date and time of the update
        :return:
        """
        # Add friend in database
        friend = self.add_friend(follower.screen_name, follower.description, follower.location,
                                 follower.followers_count, follower.friends_count, follower.statuses_count)

        # If follower doesn't exist
        if not self.follower_exists(follower):
            new_follower = Follower(follower_friend=friend.friend_id, follower_last_update=update_time)
            self._session.add(new_follower)
            return True
        else:
            update(Follower).where(Follower.follower_friend.friend_screen_name == follower.screen_name).\
                values(follower_last_update=update_time)
            return False
        # end if
    # end add_follower

    # Add a following
    def add_following(self, following, update_time=datetime.datetime.now()):
        """
        Add following
        :param following:
        :param update_time: Date and time of the update
        :return:
        """
        # Add to friend in DB
        friend = self.add_friend(following)

        # If following doesn't exists
        if not self.following_exists():
            new_following = Following(following_friend=friend, following_last_update=update_time)
            self._session.add(new_following)
            return True
        else:
            update(Following).where(Following.following_friend.friend_screen_name == following.screen_name). \
                values(following_last_update=update_time)
            return False
        # end if
    # end add_following

    # Update the list of followers
    def update_followers(self, update_time=datetime.datetime.now()):
        """
        Update the list of followers
        """
        # Get follower cursor
        cursor = self._twitter_con.get_followers_cursor()

        # Add count
        add_count = 0

        # For each page
        for page in cursor:
            # For each follower
            for follower in page:
                add_count += FriendsManager().add_follower(follower, update_time)
            # end for
            # Commit and wait
            self._session.commit()
            time.sleep(60)
        # end for

        return add_count
    # end update_followers

    # Update the list of following
    def update_following(self, update_time=datetime.datetime.now()):
        """
        Update the list of followings
        :param update_time: Date and time of the last update.
        """
        # Get follower cursor
        cursor = self._twitter_con.get_followers_cursor()

        # Add count
        add_count = 0

        # For each page
        for page in cursor:
            # For each following
            for following in page:
                add_count += FriendsManager().add_following(following, update_time)
            # end for
            # Commit and wait
            self._session.commit()
            time.sleep(60)
        # end for

        return add_count
    # end update_following

    # Update followers and following
    def update(self):
        """
        Update followers and following
        :return:
        """
        # Time of the update
        update_time = datetime.datetime.now()

        # Update followers
        new_follower_count = self.update_followers(update_time)

        # Update following
        new_following_count = self.update_following(update_time)

        # Delete old
        self._delete_followers(update_time)
        self._delete_following(update_time)

        return new_follower_count, new_following_count
    # end update

    # Delete followers
    def _delete_followers(self, update_time):
        """
        Delete followers
        :param update_time:
        :return:
        """
        delete(Follower).where(Follower.follower_last_update != update_time)
    # end _delete_followers

    # Delete following
    def _delete_following(self, update_time):
        """
        Delete following
        :param update_time:
        :return:
        """
        delete(Following).where(Following.following_last_update != update_time)
    # end _delete_followers

# end FriendsManager
