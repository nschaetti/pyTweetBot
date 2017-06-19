#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Import
from .Hunter import Hunter
from news.GoogleNewsClient import GoogleNewsClient


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

    # end next

# end GoogleNewsHunter
