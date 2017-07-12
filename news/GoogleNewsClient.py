#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Import
import urllib2
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import numpy as np
import time
import random
from .NewsParser import NewsParser
import logging


#
# This is a Google News client
# Which return an array containing the urls and titles
#
class GoogleNewsClient(object):
    """
    This a a Google News client.
    Which returns an array containing the URLs and titles.
    """

    # constructor
    def __init__(self, keyword, lang, country):
        """
        Constructor
        :param keyword:
        :param lang:
        :param country:
        """
        # Parameters
        self.keyword = keyword
        self.lang = lang
        self.country = country
    # end constructor

    ###############################################
    #
    # Public functions
    #
    ###############################################

    # Get news
    def get_news(self, page=0):
        """
        Get news
        :param page: Page to get
        :return: Array of news
        """
        # Init
        news = []

        # Logging
        logging.debug(u"Getting page {}".format(page))

        # Add page's news
        news += self._get_page(page)

        # Wait for random time
        time.sleep(random.randint(15, 35))

        return news
    # end get_news

    ###############################################
    #
    # Private functions
    #
    ###############################################

    # Get news' title
    @staticmethod
    def _get_news_title(url):
        """
        Get the news' title
        :param url: The news' URL.
        :return: The title
        """
        # HTML parser
        pars = HTMLParser()

        # Get URL's content
        soup = BeautifulSoup(urllib2.urlopen(url, timeout=10000), "lxml")

        # Clean strange characters
        new_title = unicode(soup.title.string.strip())
        new_title = new_title.replace(u'\n', u'').replace(u'\t', u'').replace(u"'", u"\'").replace(u"&amp;",
                                                                                                   u"&").replace(u'\r',
                                                                                                                 u'')
        new_title = new_title.replace(u'â&euro;&trade;', u"\'").replace(u'&#8217;', u"\'").replace(u'&#39;',
                                                                                                   u"\'").replace(
            u'&#039;', u"\'")
        new_title = new_title.replace(u'&#x27;', u'\\').replace(u'&rsquo;', u"\'").replace(u"  ", u" ")
        new_title = pars.unescape(new_title)

        # Return
        return new_title
    # end get_news_title

    # Get page
    def _get_page(self, page):
        """
        Get a page
        :param page: Page number
        :return: Page's news as an array.
        """
        # Init
        news = []

        # Call URL
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"}
        request = urllib2.Request(
            "https://www.google.ch/search?hl=" + self.lang + "&gl=" + self.country + "&q=" + self.keyword.replace(" ",
                                                                                                                  "+") + "&tbm=nws&start=" + str(
                page * 10), None, headers)
        html = urllib2.urlopen(request, timeout=5).read()

        # instantiate the parser and fed it some HTML
        parser = NewsParser()
        parser.feed(html)
        urls = parser.get_news()

        # For each url
        for url in urls:
            # Get title
            try:
                title = self._get_news_title(url)
                news.append((url, title))
            except urllib2.HTTPError:
                continue
            except:
                continue
            # end try
        return news
    # end _get_page
# end GoogleNewsClient
