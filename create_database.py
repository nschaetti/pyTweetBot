#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : create_database.py
# Description : Create database.
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

import db.obj
from sqlalchemy import create_engine


# Function to create the database
def create_database(config):
    """
    Function to create the database.
    :param config: The bot configuration object
    """
    # Settings
    host = config.database['host']
    user = config.database['username']
    password = config.database['password']
    db_name = config.database['database']

    # Create an engine that stores data in the local directory's
    engine = create_engine("mysql://{}:{}@{}/{}".format(user, password, host, db_name))

    # Create all tables in  the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    db.obj.Base.metadata.create_all(engine, checkfirst=True)
# end create_database
