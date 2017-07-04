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
import argparse
import logging

from config.BotConfig import BotConfig
from db.DBConnector import DBConnector
from executor.ActionScheduler import ActionScheduler
from friends.FriendsManager import FriendsManager
from tweet.RSSHunter import RSSHunter
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.TweetFinder import TweetFinder
from twitter.TweetBotConnect import TweetBotConnector
from twitter.TweetGenerator import TweetGenerator
from tweet.TweetFactory import TweetFactory

####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="pyTweetBot - Smart Tweeter Bot")

    # Argument
    parser.add_argument("--action", type=str, help="What to do (execute, dm, friends, news, retweet).")
    parser.add_argument("--config", type=str, help="Configuration file", required=True)
    parser.add_argument("--log-level", type=int, help="Log level", default=20)
    args = parser.parse_args()

    # Logging
    logging.basicConfig(level=args.log_level)
    logger = logging.getLogger(name="pyTweetBot")

    # Load configuration file
    config = BotConfig.load(args.config)

    # Connection to MySQL
    dbc = config.get_database_config()
    mysql_connector = DBConnector(host=dbc["host"], username=dbc["username"], password=dbc["password"],
                                  db_name=dbc["database"])

    # Connection to Twitter
    twitter_connector = TweetBotConnector(config)

    # Friends
    friends_manager = FriendsManager()
    #n_follower, d_follower, n_following, d_following = friends_manager.update()
    #logger.info("%d new follower, %d unfollow, %d new following, %d unfollowing")
    """obsolete_friends = friends_manager.get_obsolete_friends(days=14)
    logger.info("Obsolete friends : ")
    for friend in obsolete_friends:
        print(friend.friend_screen_name)
        print(friend.friend_following_date)
    # end for"""

    # Action scheduler
    action_scheduler = ActionScheduler()

    # Add until reservoir is full
    """index = 433
    while True:
        try:
            action_scheduler.add_follow(index)
        except ActionAlreadyExists as e:
            print(e)
            break
        # end tryp
        index += 1
    # end while"""
    """for action in action_scheduler.get_exec_action():
        action.execute()
    # end for"""
    #action_scheduler.add_tweet("http://www.nilsschaetti.com")
    #action_scheduler.add_tweet("This is a test for #pyTweetBot https://github.com/nschaetti/pyTweetBot")
    #action_scheduler()

    #friends_manager.update_statistics()

    # Tweet generator
    tweet_factory = TweetFactory(config.get_hashtags())
    action_scheduler.set_factory(tweet_factory)

    # Tweet finder
    tweet_finder = TweetFinder()
    for rss_stream in config.get_rss_streams():
        tweet_finder.add(RSSHunter(rss_stream))
    # end for
    #tweet_finder.add(RSSHunter("http://feeds.feedburner.com/TechCrunch/startups"))
    #tweet_finder.add(RSSHunter("http://feeds.feedburner.com/TechCrunch/fundings-exits"))
    #tweet_finder.add(RSSHunter("http://feeds.feedburner.com/TechCrunch/social"))
    tweet_finder.add(GoogleNewsHunter(search_term="machine learning", lang="en", country="us"))

    # Tweet preparator
    #tweet_preparator = TweetPreparator(config.get_hashtags())

    # For each tweet
    for tweet in tweet_finder:
        #action_scheduler.add_tweet(tweet)
        print(unicode(tweet_factory(tweet)).encode('ascii', errors='ignore'))
        print(unicode(tweet.get_tweet()).encode('ascii', errors='ignore'))
        print(len(tweet.get_tweet()) + 24)
        print("")
    # end for

# end if
