#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
from textblob import TextBlob
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
    def __init__(self, search_term, lang, country, hashtags, n_pages=2):
        """
        Constructor
        :param search_term: Search term
        :param lang: Language
        :param lang_type: Sub-language
        """
        self._search_term = search_term
        self._lang = lang
        self._country = country
        self._hashtags = hashtags
        self._n_pages = n_pages
        self._google_news_client = GoogleNewsClient(search_term, lang, country)
        self._news = list()
        self._current_page = 0
    # end __init__

    # To unicode
    def __unicode__(self):
        """
        To unicode
        :return:
        """
        return u"GoogleNewsHunter(search_term={})".format(self._search_term)
    # end __unicode__

    # Iterator
    def __iter__(self):
        """
        Iterator
        :return: Iterator
        """
        return self
    # end __iter__

    # Next element
    def next(self):
        """
        Next element
        :return:
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
        print(self._lang)
        if tweet_blob.detect_language() in self._lang:
            # Return
            return Tweet(text=current_news[1], url=current_news[0], hashtags=self._hashtags)
        else:
            logging.getLogger(pystr.LOGGER).debug(
                pystr.DEBUG_WRONG_LANGUAGE.format(current_news[1], tweet_blob.detect_language(), self._lang)
            )
            return self.next()
        # end if
    # end next

# end GoogleNewsHunter
