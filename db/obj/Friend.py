#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Friend.py
# Description : pyTweetBot friend class in the DB.
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

# Import
import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean
from sqlalchemy.types import Enum
from .Base import Base


# Friend (follower/following) in the database
class Friend(Base):
    """
    Friend (follower/following) in the database
    """

    # Table name
    __tablename__ = "pytwb_friends"

    # Fields
    friend_id = Column(BigInteger, primary_key=True, autoincrement=True)
    friend_screen_name = Column(String(100), nullable=False, unique=True)
    friend_description = Column(String(1000), nullable=False)
    friend_location = Column(String(100), nullable=False)
    friend_follower = Column(Boolean, nullable=False, default=False)
    friend_following = Column(Boolean, nullable=False, default=False)
    friend_follower_date = Column(DateTime, nullable=True, default=None)
    friend_following_date = Column(DateTime, nullable=True, default=None)
    friend_followers_count = Column(Integer, nullable=False, default=0)
    friend_friends_count = Column(Integer, nullable=False, default=0)
    friend_statuses_count = Column(Integer, nullable=False, default=0)
    friend_special = Column(Boolean, nullable=False, default=False)
    friend_contacted = Column(Boolean, nullable=False, default=False)
    friend_last_update = Column(DateTime, nullable=False, default=datetime.datetime.now())

    ######################################################
    # PROPERTIES
    ######################################################

    # Is the friend a follower?
    @property
    def follower(self):
        """
        Is the friend a follower?
        :return: True if follower, False otherwise
        """
        return self.friend_follower
    # end follower

    # Set the friend as follower
    @follower.setter
    def follower(self, follow):
        """
        Set the friend as follower
        :param follow: True if set as follower, False if not
        """
        # Something to change?
        if follow != self.follower:
            # Change
            self.friend_follower = follow
        # end if
    # end follower

    # Is the friend a following
    @property
    def following(self):
        """
        Is the friend a following
        :return: True if following, False otherwise
        """
        return self.friend_following
    # end is_following

    # Set the friend as following
    @following.setter
    def following(self, following):
        """
        Set the friend as following
        :param following: True if following, False otherwise
        """
        # Something to change
        if following != self.following:
            # Change
            self.friend_following = following
        # end if
    # end following

    ######################################################
    # PUBLIC FUNCTIONS
    ######################################################

    ######################################################
    # OVERRIDE
    ######################################################

    # To string
    def __str__(self):
        """
        To string
        :return:
        """
        return "Friend(id={}, screen_name={}, description={}, follower={}, following={})".format(
            self.friend_id,
            self.friend_screen_name,
            self.friend_description,
            self.friend_follower,
            self.friend_following)
    # end __str__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"Friend(id={}, screen_name={}, description={}, follower={}, following={})".format(
            self.friend_id,
            self.friend_screen_name,
            self.friend_description,
            self.friend_follower,
            self.friend_following)
    # end __unicode__

    ######################################################
    # STATIC FUNCTIONS
    ######################################################

    # Get a friend by it's screen name or id
    @staticmethod
    def get_friend(name_or_id):
        """
        Get a friend by it's screen name
        :param name_or_id:
        :return:
        """
        if type(name_or_id) == int:
            pass
        elif type(name_or_id) == str or type(name_or_id) == unicode:
            pass
        # end if
    # end get_friend

# end Friend
