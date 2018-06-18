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
import os
import sys
from learning.Dataset import Dataset
from tweet.GoogleNewsHunter import GoogleNewsHunter
from tweet.RSSHunter import RSSHunter
from tweet.TweetFinder import TweetFinder
from tools.PageParser import PageParser, PageParserRetrievalError


####################################################
# Main function
####################################################


# Create a tweet dataset
def tweet_dataset(config, dataset_file, n_pages, info, rss):
    """
    Create a tweet dataset
    :param config:
    :param tweet_connector:
    :return:
    """
    # Load or create dataset
    if os.path.exists(dataset_file):
        print(u"Opening dataset file {}".format(dataset_file))
        dataset = Dataset.load(dataset_file)
    else:
        dataset = Dataset()
    # end if

    # Show informations
    if info:
        print(dataset)
        exit()
    # end if

    # Tweet finder
    tweet_finder = TweetFinder(shuffle=True)

    if rss == "":
        # Add RSS streams
        for rss_stream in config.rss:
            tweet_finder.add(RSSHunter(rss_stream))
        # end for

        # Add Google News
        for news in config.get_news_config():
            for language in news['languages']:
                for country in news['countries']:
                    tweet_finder.add(
                        GoogleNewsHunter(search_term=news['keyword'], lang=language, country=country, n_pages=n_pages))
                # end for
            # end for
        # end for
    else:
        tweet_finder.add(RSSHunter({'url': rss, 'hashtags': []}))
    # end if

    # For each tweet
    for tweet in tweet_finder:
        # Get page's text
        try:
            page_text = PageParser.get_text(tweet.get_url())
        except PageParserRetrievalError as e:
            sys.stderr.write(u"Page retrieval error : {}".format(e))
            continue
        # end try

        # Not already in dataset
        if not dataset.is_in(page_text):
            # Ask
            print(u"Would you classify the following element as negative(n) or positive(p)?")
            print(u"Text : {}".format(tweet.get_text()))
            print(u"URL : {}".format(tweet.get_url()))
            observed = raw_input(u"Positive or negative (p/n) (q for quit, s for skip) : ").lower()

            # Add as example
            if observed == 'q':
                break
            elif observed == 'p':
                dataset.add_positive(page_text)
            elif observed == 's':
                pass
            else:
                dataset.add_negative(page_text)
            # end if

            # Save dataset
            dataset.save(dataset_file)
        else:
            logging.debug(u"Is already in the dataset : {}".format(tweet.get_url()))
        # end if
    # end for

# end if
