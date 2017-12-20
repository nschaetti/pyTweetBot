#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : tools.strings.py
# Description : Error, logs strings.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 19.12.2017 17:59:05
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

# Logger's name
LOGGER = u"pyTweetBot"

#########################################
# ERRORS
#########################################

# Parsing configuration file
ERROR_PARSING_CONFIG_FILE = u"Error parsing configuration file : {}\n"

# Reservoir full
ERROR_RESERVOIR_FULL = u"Reservoir full for Tweet action, exiting..."

# Tweet already in DB
ERROR_TWEET_ALREADY_DB = u"Tweet \"{}\" already exists in the database"
ERROR_RETWEET_ALREADY_DB = u"Retweet \"{}\" already exists in the database"

# Unknown source
ERROR_UNKNOWN_SOURCE = u"Unknown source {}!\n"

# Unknown training action
ERROR_UNKNOWN_TRAINING = u"Unknown training action {}\n"

# Unknown command
ERROR_UNKNOWN_COMMAND = u"Unknown command {}\n"

# Retrieving page error
ERROR_RETRIEVING_PAGE = u"Error while retrieving page {} : {}"

# Title is too short
ERROR_TITLE_TOO_SHORT_BAD_LANGUAGE = u"Title is too short ({}) or wrong language ({})"

# Not enough page data
ERROR_NOT_ENOUGH_PAGE_DATA = u"Not enough page data ({})"

#########################################
# WARNINGS
#########################################

# Page retrieval warning
WARNING_PAGE_RETRIEVAL = u"Page retrieval error : {}"

##########################################
# INFO
##########################################

# Adding tweet to DB
INFO_ADD_TWEET_SCHEDULER = u"Adding Tweet \"{}\" to the scheduler"
INFO_ADD_RETWEET_SCHEDULER = u"Adding Tweet \"{}\" to the scheduler"

# Twitter wait time
INFO_TWITTER_WAIT = u"Wait 60 seconds (Twitter limits)"
