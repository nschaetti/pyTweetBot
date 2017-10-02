#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : twitter.PyTweetBotConnector.py
# Description : pyTweetBot Twitter connector.
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

import tweepy
import time
import logging
from patterns.singleton import singleton


# Twitter connector
@singleton
class TweetBotConnector(object):
    """
    Twitter Connector
    """

    # Constructor
    def __init__(self, bot_config=None):
        """
        Constructor
        :param bot_config: Bot configuration object.
        """
        # Auth to Twitter
        config = bot_config.get_twitter_config()
        auth = tweepy.OAuthHandler(config['auth_token1'], config['auth_token2'])
        auth.set_access_token(config['access_token1'], config['access_token2'])
        self._api = tweepy.API(auth)
        self._cursor = tweepy.Cursor(self._api.followers).pages()
        self._page = None
        self._followers = list()
        self._current_follower = 0
        self._config = config
    # end __init__

    ###########################################
    # Public
    ###########################################

    # Retweet
    def retweet(self, tweet_id):
        """
        Retweet
        :param tweet_id: Tweet's ID.
        """
        logging.getLogger(u"pyTweetBot").info(u"Retweeting {}".format(tweet_id))
        self._api.retweet(tweet_id)
    # end retweet

    # Tweet
    def tweet(self, text):
        """
        Send a Tweet
        :param text: Tweet's text.
        """
        try:
            logging.getLogger(u"pyTweetBot").info(u"Tweeting \"{}\"".format(text))
            self._api.update_status(status=text)
        except tweepy.error.TweepError as e:
            logging.getLogger(u"pyTweetBot").info(u"Twitter API error \"{}\"".format(e))
        # end try
    # end tweet

    # Unfollow
    def unfollow(self, screen_name):
        """
        Unfollow
        :param user_id: Twitter user's ID to follow.
        """
        logging.getLogger(u"pyTweetBot").info(u"Unfollowing Twitter username {}".format(screen_name))
        self._api.destroy_friendship(screen_name)
    # end unfollow

    # Follow
    def follow(self, screen_name):
        """
        Follow a user.
        :param user_id:
        """
        logging.getLogger(u"pyTweetBot").info(u"Following Twitter username {}".format(screen_name))
        self._api.create_friendship(screen_name)
    # end follow

    # Like
    def like(self, tweet_id):
        """
        Like a tweet.
        :param tweet_id: Tweet's ID.
        """
        logging.getLogger(u"pyTweetBot").info(u"Liking Tweet {}".format(tweet_id))
        self._api.create_favorite(tweet_id)
    # end like

    # Send direct message
    def send_direct_message(self, user_id, text):
        """
        Send direct message.
        :param user_id: Receipe user's ID.
        :param text: Message's text.
        """
        logging.getLogger(u"pyTweetBot").info(u"Sending message \"{}\" to {}".format(text, user_id))
        self._api.send_direct_message(user_id=user_id, text=text)
    # end send_direct_message

    # Get time line
    def get_time_line(self, n_pages):
        """
        Get time line.
        :param n_pages:
        :return:
        """
        return tweepy.Cursor(self._api.home_timeline, screen_name='nschaetti').pages(limit=n_pages)
    # end get_time_line

    # Get user timeline
    def get_user_timeline(self, screen_name, n_pages=-1):
        """
        Get time line.
        :param n_pages:
        :return:
        """
        if n_pages == -1:
            return tweepy.Cursor(self._api.user_timeline, screen_name=screen_name).pages()
        else:
            return tweepy.Cursor(self._api.user_timeline, screen_name=screen_name).pages(limit=n_pages)
        # end if
    # end get_time_line

    # Ger search cursor
    def search_tweets(self, search, n_pages=-1):
        """
        Get search cursor
        :param search:
        :param n_pages:
        :return:
        """
        if n_pages == -1:
            return tweepy.Cursor(self._api.search, q=search).pages()
        else:
            return tweepy.Cursor(self._api.search, q=search).pages(limit=n_pages)
        # end if
    # end search_tweets

    # Get followers
    def get_followers(self, n_pages=-1):
        """
        Get followers
        :return:
        """
        follower_list = list()
        page_count = 0
        # For each pages
        for page in tweepy.Cursor(self._api.followers).pages():
            # For each follower in the page
            for follower in page:
                follower_list.append(follower)
            # end for

            # Inc
            page_count += 1

            # Limit
            if n_pages != -1 and page_count >= n_pages:
                break
            # end if

            # Wait 60s
            time.sleep(60)
        # end for
        return follower_list
    # end get_followers

    # Reset
    def reset(self):
        self._cursor = None
        self._page = None
    # end reset

    # Get followers cursor
    def get_followers_cursor(self):
        """
        Get followers cursor.
        :return: Followers cursor.
        """
        return tweepy.Cursor(self._api.followers)
    # end get_followers_cursor

    # Get following cursor
    def get_following_cursor(self):
        """
        Get following cursor.
        :return: Following cursor.
        """
        return tweepy.Cursor(self._api.friends)
    # end get_followers_cursor

    # Get the user
    def get_user(self, screen_name=None):
        """
        Get the user
        :return: The Twitter user object.
        """
        if screen_name is None:
            return self._api.get_user(self._config['user'])
        else:
            return self._api.get_user(screen_name)
        # end if
    # end get_user

    ###########################################
    # Override
    ###########################################

    def next(self):
        # Follower
        follower = self._followers[self._current_follower]

        # Next follower
        self._current_follower += 1
        if self._current_follower >= len(self._followers):
            self._load_followers()
        # end if

        return follower
    # end next

    ###########################################
    # Private
    ###########################################

    # Load followers
    def _load_followers(self):
        self._page = self._cursor.next()
        self._followers = list()
        for follower in self._page:
            self._followers.append(follower)
        # end for
        self._current_follower = 0
        time.sleep(60)
    # end load

# end TweetBotConnector
