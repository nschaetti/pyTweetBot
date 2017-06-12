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
from sqlalchemy import update


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
    def get_friend(self, friend):
        """
        Get a friend from the DB.
        :param friend: The friend to get as a Tweepy object.
        :return: The friend DB object.
        """
        print(friend)
        return self._session.query(Friend).filter(Friend.friend_screen_name == friend.friend_screen_name).one()
    # end get_friend

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
    def exists(self, friend):
        """
        Follower exists.
        :param friend:
        :return:
        """
        if len(self._session.query(Friend).filter(Friend.friend_screen_name == friend.screen_name).all()) > 0:
            return True
        # end if
        return False
    # end exists

    # Follower exists
    def follower_exists(self, follower):
        """
        The follower exists in the DB.
        :param follower:
        :return:
        """
        # Friend
        friend = self.get_friend(follower)

        # Friend exists
        if friend is not None:
            if len(self._session.query(Follower).filter(Follower.follower_friend == friend).all()) > 0:
                return True
            # end if
        # end if
        return False
    # end follower_exists

    # Following exists
    def following_exists(self, following):
        """
        The following exists
        :param following:
        :return:
        """
        # Friend
        friend = self.get_friend(following)

        # Friend exists
        if friend is not None:
            if len(self._session.query(Following).filter(Following.following_friend == friend).all()) > 0:
                return True
            # end if
        # end if
        return False
    # end following_exists

    # Add a friend
    def add_friend(self, friend):
        """
        Add a friend to the db
        :param friend: The friend to add as a Tweepy object.
        :return: The new friend DB object.
        """
        if not self.exists(friend):
            new_friend = Friend(friend_screen_name=friend.screen_name, friend_description=friend.description,
                                friend_location=friend.location, friend_followers_count=friend.followers_count,
                                friend_friends_count=friend.friends_count, friend_statuses_count=friend.statuses_count)
            self._session.add(new_friend)
            return new_friend
        else:
            return self.get_friend(friend)
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
        # Add in friends database
        friend = self.add_friend(follower)

        # If follower doesn't exist
        if not self.follower_exists(friend):
            new_follower = Follower(follower_friend=friend, follower_last_update=update_time)
            self._session.add(new_follower)
        else:
            update(Follower).where(Follower.follower_friend.friend_screen_name == follower.screen_name).\
                values(follower_last_update=update_time)
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
        # end if
    # end add_following

    # Update the list of followers
    def update_followers(self, update_time=datetime.datetime.now()):
        """
        Update the list of followers
        """
        # Get follower cursor
        cursor = self._twitter_con.get_followers_cursor()

        # For each page
        for page in cursor:
            # For each follower
            for follower in page:
                FriendsManager().add_follower(follower, update_time)
            # end for
        # end for
        self._session.commit()
    # end update_followers

    # Update the list of following
    def update_following(self, update_time=datetime.datetime.now()):
        """
        Update the list of followings
        :param update_time: Date and time of the last update.
        """
        pass
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
        self.update_followers(update_time)

        # Update following
        self.update_following(update_time)
    # end update

# end FriendsManager
