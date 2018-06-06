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
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .Base import Base
from .Friend import Friend


# Following
class Following(Base):
    """
    Following
    """

    # Table name
    __tablename__ = "pytwb_following"

    # Fields
    following_id = Column(BigInteger, primary_key=True, autoincrement=True)
    following_friend = Column(BigInteger, ForeignKey('pytwb_friends.friend_id'), nullable=False)
    follower_followed_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
    following_last_update = Column(DateTime, nullable=False, default=datetime.datetime.now())

    # Relationships
    friend = relationship(Friend)

# end Following
