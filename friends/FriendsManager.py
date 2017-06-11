#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from patterns.singleton import singleton
from db.DBConnector import DBConnector
from db.Friend import Friend
from twitter.TweetBotConnect import TweetBotConnector


@singleton
class FriendsManager(object):

    # Get followers
    @staticmethod
    def get_followers():
        """
        Get followers
        :return: Follower list
        """
        session = DBConnector().get_session()
        return session.query(Friend).all()
    # end get_followers

    # Follower exists
    @staticmethod
    def exists(follower):
        """
        Follower exists.
        :param follower:
        :return:
        """
        session = DBConnector().get_session()
        if len(session.query(Friend).filter(Friend.friend_screen_name == follower.screen_name).all()) > 0:
            return True
        # end if
        return False
    # end exists

    # Add a follower
    @staticmethod
    def add_follower(follower):
        """
        Add follower
        :param follower: Twitter follower
        :return:
        """
        session = DBConnector().get_session()
        new_friend = Friend(friend_screen_name=follower.screen_name, friend_description=follower.description,
                            friend_location=follower.location, friend_direction="In")
        session.add(new_friend)
    # end add_follower

    # Update
    @staticmethod
    def update():
        """
        Update
        :return:
        """
        # DB session
        session = DBConnector().get_session()

        # Twitter connection
        twitter_con = TweetBotConnector()

        # Get follower cursor
        cursor = twitter_con.get_followers_cursor()

        # For each page
        for page in cursor:
            # For each follower
            for follower in page:
                print(follower.description)
                if not FriendsManager().exists(follower):
                    FriendsManager().add_follower(follower)
                else:
                    session.commit()
                    return
                # end if
            # end for
        # end for
        session.commit()
    # end update

# end FriendsManager
