#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
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
import logging
import signal
import os
import time
import sys
import nsNLP
from github import Github
from executor.ActionScheduler import ActionReservoirFullError, ActionAlreadyExists
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from tweet.TweetFactory import TweetFactory
from learning.CensorModel import CensorModel
from news.PageParser import PageParser, PageParserRetrievalError
from twitter.TweetBotConnect import TweetBotConnector
import db.obj

####################################################
# Globals
####################################################

# Continue main loop?
cont_loop = True

####################################################
# Functions
####################################################


# Signal handler
def signal_handler(signum, frame):
    """
    Signal handler
    :param signum:
    :param frame:
    :return:
    """
    global cont_loop
    logging.info(u"Signal {} received in frame {}".format(signum, frame))
    cont_loop = False
# end signal_handler


# Prepare project name
def prepare_project_name(project_name):
    """
    Prepare project name
    :param project_name:
    :return:
    """
    project_name = project_name.replace(u'-', u' ')
    if u' ' in project_name:
        project_name = project_name.title()
    # end if
    return project_name.replace(u' ', u'')
# end prepare_project_name


# Create tweet text
def create_tweet_text(contrib_counter, contrib_date, project_name, project_url, topics):
    """

    :param contrib_counter:
    :param contrib_date:
    :param project_name:
    :param project_url:
    :param topics:
    :return:
    """
    # Tweet text
    tweet_text = u"I made {} contributions on {} to project #{}, #GitHub".format\
    (
            contrib_counter,
            contrib_date.strftime('%B %d'),
            project_name
    )

    # For each topics
    for topic in topics:
        if len(u"{} #{}".format(tweet_text, topic)) + 21 < 140:
            tweet_text = u"{} #{}".format(tweet_text, topic)
        else:
            break
        # end if
    # end for

    return u"{} {}".format(tweet_text, project_url)
# end create_tweet_text


# Create tweet text for repo creation
def create_tweet_text_create(project_name, project_description, project_url, topics):
    """
    Create tweet text for repo creation
    :param project_name:
    :param project_description:
    :param project_url:
    :param topics:
    :return:
    """
    # Tweet text
    tweet_text = u"Check my project {} on #GitHub : {}".format \
    (
        project_name,
        project_description
    )

    # Check Tweet length
    if len(tweet_text) + 21 > 180:
        # Not wanted chars
        overflow_text = 180 - (len(tweet_text) + 21)

        # Remove
        tweet_text = tweet_text[:-overflow_text-3] + u"..."
    # end if

    # Add topics
    for topic in topics:
        if len(u"{} #{}".format(tweet_text, topic)) + 21 < 140:
            tweet_text = u"{} #{}".format(tweet_text, topic)
        else:
            break
        # end if
    # end for

    # Return with URL
    return u"{} {}".format(tweet_text, project_url)
# end create_tweet_text_create


# Add tweet to scheduler
def add_tweet(action_scheduler, tweet_text):
    """
    Add tweet to scheduler
    :param action_scheduler:
    :param tweet_text:
    :return:
    """
    # Add to scheduler
    try:
        logging.getLogger(u"pyTweetBot").info(u"Adding GitHub Tweet \"{}\" to the scheduler".format(
            tweet_text))
        action_scheduler.add_tweet(tweet_text)
        return True
    except ActionReservoirFullError:
        logging.getLogger(u"pyTweetBot").error(u"Reservoir full for Tweet action, exiting...")
        exit()
        pass
    except ActionAlreadyExists:
        logging.getLogger(u"pyTweetBot").error(
            u"Tweet \"{}\" already exists in the database".format(
                tweet_text.encode('ascii', errors='ignore')))
        return False
    # end try
# end add_tweet


####################################################
# Main function
####################################################

# Find Github informations to tweet
def find_github_tweets(config, action_scheduler, event_type="push", depth=-1, instantaneous=False, waiting_time=0):
    """
    Find tweet in the hunters
    :param config:
    :param model:
    :param action_scheduler:
    :return:
    """
    # Github settings
    github_settings = config.get_github_config()

    # Login info
    login = github_settings['login']
    password = github_settings['password']
    exclude = github_settings['exclude']
    topics = github_settings['topics']

    # Connection
    g = Github(login, password)

    # For each repositories
    for repo in g.get_user().get_repos():
        # No private repositories
        if not repo.private and repo.name not in exclude:
            # Project's name
            project_name = prepare_project_name(repo.name)
            project_url = u"https://github.com/{}/{}".format(login, project_name, repo.name)
            project_description = repo.description

            # Topics
            if repo.name in topics:
                project_topics = topics[repo.name]
            else:
                project_topics = []
            # end if

            # Counter and date
            contrib_counter = 0
            contrib_date = None
            tweet_count = 0

            # For each events
            for event in repo.get_events():
                # Only pushes
                if event.type == u"PushEvent" and event_type == "push":
                    # Same day?
                    if contrib_date is not None and event.created_at.year == contrib_date.year and event.created_at.month == contrib_date.month and event.created_at.day == contrib_date.day:
                        contrib_counter += 1
                    else:
                        # Something to tweet?
                        if contrib_date is not None:
                            # Tweet text
                            tweet_text = create_tweet_text(contrib_counter, contrib_date, project_name, project_url, project_topics)

                            # Add to scheduler
                            # if not instantaneous
                            if not db.obj.Tweeted.exists(tweet_text):
                                if not instantaneous:
                                    if not add_tweet(action_scheduler, tweet_text):
                                        break
                                    # end if
                                else:
                                    TweetBotConnector().tweet(tweet_text)
                                    db.obj.Tweeted.insert_tweet(tweet_text)
                                # end if
                            # end if

                            # Waiting time
                            if waiting_time > 0:
                                time.sleep(waiting_time)
                            # end if

                            # Check depth
                            tweet_count += 1
                            if depth != -1 and tweet_count >= depth:
                                break
                            # end if
                        # end if

                        # Reset counter and date
                        contrib_counter = event.payload['size']
                        contrib_date = event.created_at
                elif event.type == u"CreateEvent" and event_type == "create":
                    # Tweet text
                    tweet_text = create_tweet_text_create(project_name, project_description, project_url, project_topics)

                    # Add to scheduler
                    add_tweet(action_scheduler, tweet_text)
                # end if
            # end for
        # end if
    # end for

# end if
