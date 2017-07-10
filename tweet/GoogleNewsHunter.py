#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
from .Hunter import Hunter
from news.googlenewsclient import GoogleNewsClient
from .Tweet import Tweet


# Hunter for Google News
class GoogleNewsHunter(Hunter):
    """
    An hunter for Google News
    """

    # Constructor
    def __init__(self, search_term, lang, country, n_pages=2):
        """
        Constructor
        :param search_term: Search term
        :param lang: Language
        :param lang_type: Sub-language
        """
        self._search_term = search_term
        self._lang = lang
        self._country = country
        self._n_pages = n_pages
        self._google_news_client = GoogleNewsClient(search_term, lang, country)
        self._news = list()
        self._current_page = 0
    # end __init__

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
            self._current_page += 1
            if self._current_page > self._n_pages:
                raise StopIteration
            # end if
            self._news = self._google_news_client.get_news(page=self._current_page-1)
        # end if

        # Current news
        current_news = self._news[0]
        self._news.remove(current_news)

        # Return
        return Tweet(text=current_news[1], url=current_news[0])
    # end next

# end GoogleNewsHunter
