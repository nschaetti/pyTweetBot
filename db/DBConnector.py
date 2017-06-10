#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : DBConnector.py
# Description : pyTweetBot DB connector.
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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from patterns.singleton import singleton
from db.Base import Base


@singleton
class DBConnector(object):

    # Constructor
    def __init__(self, host="", username="", password="", db_name=""):
        """
        Constructor
        :param host:
        :param username:
        :param password:
        :param db_name:
        """
        self._engine = create_engine("mysql://{}:{}@{}/{}".format(username, password, host, db_name))
        Base.metadata.bind = self._engine
        db_session = sessionmaker(bind=self._engine)
        self._session = db_session()
    # end __init__

    # Call
    def get_session(self):
        """
        Call
        :return: DB session
        """
        return self._session
    # end get_session

# end PyTweetDBConnector
