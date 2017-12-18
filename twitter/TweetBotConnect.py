#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : twitter.TweetBotConnector.py
# Description : Main class to connect with Twitter API.
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

import datetime
import tweepy
import time
import logging
from patterns.singleton import singleton


# Request limits reached.
class RequestLimitReached(Exception):
    """
    Exception raised when some limits are reached.
    """
    pass
# end RequestLimitReached


# Main class to connect with Twitter API
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
        config = bot_config.twitter
        auth = tweepy.OAuthHandler(config['auth_token1'], config['auth_token2'])
        auth.set_access_token(config['access_token1'], config['access_token2'])
        self._api = tweepy.API(auth, retry_delay=3, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self._cursor = tweepy.Cursor(self._api.followers).pages()
        self._page = None
        self._followers = list()
        self._current_follower = 0
        self._config = config

        # History
        self._histories = {'follow': list(), 'unfollow': list(), 'tweet': list(), 'retweet': list(), 'like': list()}
        self._counts = {'follow': 0, 'unfollow': 0, 'tweet': 0, 'retweet': 0, 'like': 0}

        # Limits
        self._limits = dict()
        self._limits['follow'] = bot_config.friends['max_new_followers']
        self._limits['unfollow'] = bot_config.friends['max_new_unfollow']
        self._limits['tweet'] = bot_config.tweet['max_tweets']
        self._limits['retweet'] = bot_config.retweet['max_retweets']
        self._limits['like'] = bot_config.retweet['max_likes']
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
        # Log
        logging.getLogger(u"pyTweetBot").info(u"Retweeting {}".format(tweet_id))
        self._api.retweet(tweet_id)

        # Inc counter
        self._inc_counter('retweet')
    # end retweet

    # Tweet
    def tweet(self, text):
        """
        Send a Tweet
        :param text: Tweet's text.
        """
        if self.check_limits('tweet'):
            try:
                # Log
                logging.getLogger(u"pyTweetBot").info(u"Tweeting \"{}\"".format(text))
                self._api.update_status(status=text)

                # Inc counter
                self._inc_counter('tweet')
            except tweepy.error.TweepError as e:
                logging.getLogger(u"pyTweetBot").info(u"Twitter API error \"{}\"".format(e))
            # end try
        else:
            raise RequestLimitReached(u"Request limit reached for tweet action")
        # end if
    # end tweet

    # Unfollow
    def unfollow(self, screen_name):
        """
        Unfollow
        :param user_id: Twitter user's ID to follow.
        """
        if self.check_limits('unfollow'):
            # Log
            logging.getLogger(u"pyTweetBot").info(u"Unfollowing Twitter username {}".format(screen_name))
            self._api.destroy_friendship(screen_name)

            # Inc counter
            self._inc_counter('unfollow')
        else:
            raise RequestLimitReached(u"Request limit reached for unfollow action")
        # end if
    # end unfollow

    # Follow
    def follow(self, screen_name):
        """
        Follow a user.
        :param user_id:
        """
        if self.check_limits('follow'):
            # Log
            logging.getLogger(u"pyTweetBot").info(u"Following Twitter username {}".format(screen_name))
            self._api.create_friendship(screen_name)

            # Inc counter
            self._inc_counter('follow')
        else:
            raise RequestLimitReached(u"Request limit reached for follow action")
        # end if
    # end follow

    # Like
    def like(self, tweet_id):
        """
        Like a tweet.
        :param tweet_id: Tweet's ID.
        """
        if self.check_limits('like'):
            # Log
            logging.getLogger(u"pyTweetBot").info(u"Liking Tweet {}".format(tweet_id))
            self._api.create_favorite(tweet_id)

            # Inc counter
            self._inc_counter('like')
        else:
            raise RequestLimitReached(u"Request limit reached for like action")
        # end if
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

    # Check limits
    def check_limits(self, action_type):
        """
        Check limits
        :param action_type:
        :return:
        """
        # Check limits
        return self._counts[action_type] <= self._limits[action_type]
    # end check_friend_request_limits

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
        """
        Load all followers.
        :return:
        """
        self._page = self._cursor.next()
        self._followers = list()
        for follower in self._page:
            self._followers.append(follower)
        # end for
        self._current_follower = 0
        time.sleep(60)
    # end load

    # Increment counter
    def _inc_counter(self, action_type):
        """
        Increment follow counter
        :return:
        """
        # Add to history
        self._histories[action_type].append(datetime.datetime.utcnow())

        # Last 24h list
        last_day = list()
        last_day_counter = 0
        for action_time in self._histories[action_type]:
            if (datetime.datetime.utcnow() - action_time).total_seconds() <= 60 * 60 * 24:
                last_day.append(action_time)
                last_day_counter += 1
            # end if
        # end for

        # History and counter
        self._histories[action_type] = last_day
        self._counts[action_type] = last_day_counter
    # end _inc_follow_counter

# end TweetBotConnector
