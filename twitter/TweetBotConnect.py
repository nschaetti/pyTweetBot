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
        self._cursor = None
        self._page = None
    # end __init__

    # Retweet
    def retweet(self, tweet_id):
        """
        Retweet
        :param tweet_id: Tweet's ID.
        """
        self._api.retweet(tweet_id)
    # end retweet

    # Tweet
    def tweet(self, text):
        """
        Send a Tweet
        :param text: Tweet's text.
        """
        self._api.update_status(status=text)
    # end tweet

    # Unfollow
    def unfollow(self, user_id):
        """
        Unfollow
        :param user_id: Twitter user's ID to follow.
        """
        self._api.destroy_friendship(user_id)
    # end unfollow

    # Follow
    def follow(self, user_id):
        """
        Follow a user.
        :param user_id:
        """
        self._api.create_friendship(user_id)
    # end follow

    # Like
    def like(self, tweet_id):
        """
        Like a tweet.
        :param tweet_id: Tweet's ID.
        """
        self._api.create_favorite(tweet_id)
    # end like

    # Send direct message
    def send_direct_message(self, user_id, text):
        """
        Send direct message.
        :param user_id: Receipe user's ID.
        :param text: Message's text.
        """
        self._api.send_direct_message(user_id=user_id, text=text)
    # end send_direct_message

    # Get time line
    def get_time_line(self, n_pages):
        """
        Get time line.
        :param n_pages:
        :return:
        """
        c = tweepy.Cursor(self._api.home_timeline).pages(limit=n_pages)
    # end get_time_line

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

    def next(self):
        # Page cursor
        if self._page is None:
            self._cursor = tweepy.Cursor(self._api.followers).pages()
            print(self._cursor)
            self._page = self._cursor.next()
        # end if

        next_follower = self._page.next()
        if next_follower is None:
            self._page = self._cursor.next()
            next_follower = self._page.next()
        # end if

        return next_follower
    # end next

# end TweetBotConnector
