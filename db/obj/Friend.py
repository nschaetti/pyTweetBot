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


# Friend
class Friend(Base):
    """
    Friend
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
    friend_follower_date = Column(DateTime, nullable=True, default=datetime.datetime.now())
    friend_following_date = Column(DateTime, nullable=True, default=datetime.datetime.now())
    friend_followers_count = Column(Integer, nullable=False, default=0)
    friend_friends_count = Column(Integer, nullable=False, default=0)
    friend_statuses_count = Column(Integer, nullable=False, default=0)
    friend_special = Column(Boolean, nullable=False, default=False)
    friend_last_update = Column(DateTime, nullable=False, default=datetime.datetime.now())
# end Friend
