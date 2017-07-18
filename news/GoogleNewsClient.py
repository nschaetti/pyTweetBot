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
import httplib
import socket
import ssl


#
# This is a Google News client
# Which return an array containing the urls and titles
#
class GoogleNewsClient(object):
    """
    This a a Google News client.
    Which returns an array containing the URLs and titles.
    """

    # Header
    _headers = {
        u'user-agent': u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) "
                       u"AppleWebKit/537.36 (KHTML, like Gecko) "
                       u"Chrome/59.0.3071.115 "
                       u"Safari/537.36",
        u'accept': u"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        u'accept-language': u"en-US,en;q=0.8,et;q=0.6,fr;q=0.4",
        u'cache-control': u"no-cache"
    }

    # Time out
    _timeout = 20

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
    def _get_news_title(self, url):
        """
        Get the news' title
        :param url: The news' URL.
        :return: The title
        """
        # HTML parser
        pars = HTMLParser()

        # HTTP request
        request = urllib2.Request(url, None, self._headers)

        # Get HTML
        html = urllib2.urlopen(request, timeout=self._timeout).read()

        # Get URL's content
        soup = BeautifulSoup(html, "lxml")

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

        # URL
        url = u"https://www.google.ch/search?hl=" + self.lang + u"&gl=" + self.country + u"&q=" + unicode(
                self.keyword.replace(u" ", u"+")) + u"&tbm=nws&start=" + unicode(page * 10)

        # Log
        logging.info(u"Retrieving {}".format(url))

        # Call URL
        request = urllib2.Request(url, None, self._headers)

        # Get HTML
        cont = True
        counter = 0
        while cont:
            try:
                html = urllib2.urlopen(request, timeout=self._timeout).read()
                cont = False
            except urllib2.URLError as e:
                logging.error(u"URL error while retrieving page {}".format(url))
                time.sleep(20)
                pass
            # end try
            counter += 1
            if counter >= 10:
                return news
            # end if
        # end while

        # instantiate the parser and fed it some HTML
        parser = NewsParser()
        parser.feed(html.decode('utf-8', errors='ignore'))
        urls = parser.get_news()

        # For each url
        for url in urls:
            # Get title
            try:
                title = self._get_news_title(url)
                news.append((url, title))
            except urllib2.HTTPError as e:
                logging.error(u"HTTP Error while retrieving page {} : {}".format(url, e))
            except AttributeError as e:
                logging.error(u"AttributeError while retrieving page {} : {}".format(url, e))
            except httplib.BadStatusLine as e:
                logging.error(u"Bad status line error while retrieving page {} : {}".format(url, e))
            except socket.timeout as e:
                logging.error(u"Socket error while retrieving page {} : {}".format(url, e))
            except httplib.IncompleteRead as e:
                logging.error(u"Incomplete read error while retrieving page {} : {}".format(url, e))
            except urllib2.URLError as e:
                logging.error(u"Error while retrieving page {} : {}".format(url, e))
            except ssl.CertificateError as e:
                logging.error(u"Error with SSL Certificate while retrieving {} : {}".format(url, e))
            # end try
        # end for
        return news
    # end _get_page
# end GoogleNewsClient
