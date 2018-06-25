#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : GoogleNewsHunter.py
# Description : Hunt new tweets on Google News.
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
# along with pyTweetBot.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
from textblob import TextBlob
from langdetect import detect
from .Hunter import Hunter
from pyTweetBot.news.GoogleNewsClient import GoogleNewsClient
from .Tweet import Tweet
import logging
import pyTweetBot.tools.strings as pystr


# Hunter for Google News
class GoogleNewsHunter(Hunter):
    """
    An hunter for Google News
    """

    # Constructor
    def __init__(self, search_term, lang, country, hashtags, languages, n_pages=2):
        """
        Constructor

        Arguments:
            search_term (str): Term to search on Google News
            lang (str): The language code to search on Google News
            country (str): The country to search on Google News
            hashtags (list): Corresponding hashtags that will be added to the tweets
            languages (str): Which NLTK language to keep (automatically identify the language and filter it)
            n_pages (int): Number of page to take into account
        """
        self._search_term = search_term
        self._lang = lang
        self._country = country
        self._hashtags = hashtags
        self._n_pages = n_pages
        self._google_news_client = GoogleNewsClient(search_term, lang, country)
        self._news = list()
        self._current_page = 0
        self._languages = languages
    # end __init__

    # To unicode
    def __unicode__(self):
        """
        To unicode

        Returns:
            The object description
        """
        return u"GoogleNewsHunter(search_term={}, lang, country, hashtags, languages, n_pages)".format(
            self._search_term,
            self._lang,
            self._country,
            self._hashtags,
            self._languages,
            self._n_pages
        )
    # end __unicode__

    # Iterator
    def __iter__(self):
        """
        Iterator

        Returns:
            An iterator
        """
        return self
    # end __iter__

    # Next element
    def next(self):
        """
        Next element

        Returns:
            The next tweet
        """
        if len(self._news) == 0:
            if self._current_page > self._n_pages:
                raise StopIteration
            # end if
            self._news = self._google_news_client.get_news(page=self._current_page)
            self._current_page += 1
        # end if

        # Current news
        try:
            current_news = self._news[0]
        except IndexError:
            logging.getLogger(pystr.LOGGER).error(
                u"Error: no news for page {} and research terms {} ({}/{})".format(self._current_page,
                                                                                   self._search_term, self._lang,
                                                                                   self._country))
            raise StopIteration
        # end try

        # Remove from list
        self._news.remove(current_news)

        # Analyze text
        tweet_blob = TextBlob(current_news[1])

        # Check language
        if detect(current_news[1]) in self._languages:
            # Return
            return Tweet(text=current_news[1], url=current_news[0], hashtags=self._hashtags)
        else:
            logging.getLogger(pystr.LOGGER).debug(
                pystr.DEBUG_WRONG_LANGUAGE.format(current_news[1], detect(current_news[1]), self._lang)
            )
            return self.next()
        # end if
    # end next

# end GoogleNewsHunter
