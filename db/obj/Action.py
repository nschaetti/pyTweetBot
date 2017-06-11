#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : Action.py
# Description : pyTweetBot Action in the DB.
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
from sqlalchemy import Column, String, BigInteger, DateTime, Enum
from .Base import Base


# Action
class Action(Base):
    """
    Action
    """

    # Table name
    __tablename__ = "pytwb_actions"

    # Fields
    action_id = Column(BigInteger, primary_key=True)
    action_type = Column(Enum('Tweet', 'Retweet', 'Like', 'DirectMessage', 'Follow', 'Unfollow'), nullable=False)
    action_tweet_id = Column(BigInteger, nullable=False)
    action_tweet_text = Column(String(5000), nullable=False)
    action_exec_date = Column(DateTime, nullable=False)
# end Action
