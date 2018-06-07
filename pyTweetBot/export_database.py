#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : export_database.py
# Description : Export database.
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

import logging
import os
import pickle

import tools.strings as pystr


# Function to export the database
def export_database(output_dir, mysql_connector):
    """Export a database from a MySQL database to a series of files.

    Example:
        >>> export_database(".", mysql_connector)

    Arguments:
        * output_dir (str): The output directory path
        * mysql_connector (DBConnector) : A connector object of type :class:`pyTweetBot.db.DBConnector`
    """
    # Files
    actions_file = os.path.join(output_dir, u"actions.p")
    friends_file = os.path.join(output_dir, u"friends.p")
    statistics_file = os.path.join(output_dir, u"statistics.p")
    tweets_file = os.path.join(output_dir, u"tweets.p")

    # DB session
    mysql_session = mysql_connector.get_session()

    # Get from database
    actions = mysql_session.query(pytweetbot.db.obj.Action).all()
    friends = mysql_session.query(pytweetbot.db.obj.Friend).all()
    statistics = mysql_session.query(pytweetbot.db.obj.Statistic).all()
    tweets = mysql_session.query(pytweetbot.db.obj.Tweeted).all()

    # Save all
    logging.getLogger(pystr.LOGGER).info(u"Exporting data to {}".format(output_dir))
    pickle.dump(actions, open(actions_file, 'wb'))
    pickle.dump(friends, open(friends_file, 'wb'))
    pickle.dump(statistics, open(statistics_file, 'wb'))
    pickle.dump(tweets, open(tweets_file, 'wb'))
    logging.getLogger(pystr.LOGGER).info(u"Finished...")
# end export_database
