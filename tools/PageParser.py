#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Import
import socket
import sys
import urllib2
import httplib
import brotli
import gzip
import logging
from urlparse import urlparse
from bs4 import BeautifulSoup
from StringIO import StringIO
from HTMLParser import HTMLParser


# Can't retrieve page
class PageParserRetrievalError(Exception):
    """
    Exception
    """
    pass
# end PageParserRetrievalError


# Unknown encoding error
class UnknownEncoding(Exception):
    """
    Unknown encoding exception
    """
    pass
# end UnknownEncoding


#
# This is a class to retrieve text from HTML page given an URL.
#
class PageParser(object):
    """
    This is a class to retrieve text from HTML page given an URL.
    """

    # Header
    _headers = {
        u'user-agent': u"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) "
                       u"Gecko/2009021910 "
                       u"Firefox/3.0.7",
        u'accept-language': u"en-US,en;q=0.8,et;q=0.6,fr;q=0.4",
        u'cache-control': u"no-cache",
        u'authority': u"",
        u'method': u"GET",
        u'path': u"",
        u'scheme': u"http",
        u'accept': u"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        u'Accept-Charset': u'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        u'accept-encoding': u"gzip, deflate, sdch, br",
        u'pragma': u"no-cache",
        u'upgrade-insecure-requests': u"1",
        u'Connection': u'keep-alive'
    }

    # Time out
    _timeout = 20

    # Information
    _title = u""
    _html = u""

    # Constructor
    def __init__(self, url, timeout=20):
        """
        Constructor
        :param url:
        """
        # Properties
        self._url = url
        self._timeout = timeout
    # end __init__

    ###########################################
    # Properties
    ###########################################

    # Title
    @property
    def title(self):
        """
        Page's title
        :return:
        """
        return u""
    # end title

    # URL
    @property
    def url(self):
        """
        Loaded URL
        :return:
        """
        return self._url
    # end url

    # HTML code
    @property
    def html(self):
        """
        Get HTML
        :return:
        """
        return self._html
    # end html

    ###########################################
    # Public
    ###########################################

    # Reload URL
    def reload(self, url=u""):
        """
        Reload URL
        """
        if url == u"":
            self._load(self._url)
        else:
            self._load(url)
        # end if
    # end reload

    ###########################################
    # Private
    ###########################################

    # Load URL
    def _load(self, url):
        """
        Load URL
        :param url:
        :return:
        """
        # URL parser
        url_parse = urlparse(url)

        # Final header
        final_header = self._headers
        final_header[u'authority'] = url_parse.netloc
        final_header[u'path'] = url_parse.path

        # Call URL
        request = urllib2.Request(url, None, self._headers)

        # Request server
        response = urllib2.urlopen(request, timeout=self._timeout)

        # Data
        response_data = response.read()

        # Content encoding
        content_encoding = response.info().getheader('Content-Encoding')

        # Content encoding
        if content_encoding == 'br':
            data = brotli.decompress(response_data)
        elif content_encoding == 'gzip':
            buf = StringIO(response_data)
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        elif content_encoding is None or 'text/html' in content_encoding:
            data = response_data
        else:
            raise UnknownEncoding(u"Unknown encoding {}".format(content_encoding))
        # end if

        # Extract information
        self._html = data
        self._title = self._extract_title(data)
    # end _load

    # Extract title from HTML
    def _extract_title(self, html):
        """
        Extract title from HTML
        :param html:
        :return:
        """
        # HTML parser
        pars = HTMLParser()

        # Get URL's content
        soup = BeautifulSoup(html, "lxml")

        # Get and clean data
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
    # end _extract_title

# end PageParser
