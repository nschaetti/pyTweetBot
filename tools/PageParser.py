#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : mail.PageParser.py
# Description : Page parser object.
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
import urllib2
import brotli
import gzip
import socket
import sys
import urllib2
import httplib
from bs4 import BeautifulSoup
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
    _raw_title = u""
    _title = u""
    _html = u""
    _text = u""

    # Constructor
    def __init__(self, url, timeout=20):
        """
        Constructor
        :param url:
        """
        # Properties
        self._url = url
        self._timeout = timeout

        # Load URL
        self._load(url)
    # end __init__

    ###########################################
    # Properties
    ###########################################

    # Raw title
    @property
    def raw_title(self):
        """
        Raw title
        :return:
        """
        return self._raw_title
    # end raw_title

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

    # Text
    @property
    def text(self):
        """
        Get text
        :return:
        """
        return self._text
    # end text

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
        request = urllib2.Request(url.encode('ascii', errors='ignore'), None, self._headers)

        # Tries count
        count = 0
        success = False
        last_e = None

        # Try
        while count < 10:
            # Get title
            try:
                response = urllib2.urlopen(request, timeout=self._timeout)
                success = True
                break
            except urllib2.HTTPError as e:
                raise PageParserRetrievalError(u"HTTP error while retrieving {} : {}\n".format(url, e))
            except socket.error as e:
                count += 1
                last_e = e
                pass
            except urllib2.URLError as e:
                last_e = e
                count += 1
                pass
            except httplib.IncompleteRead as e:
                last_e = e
                count += 1
                pass
            except httplib.BadStatusLine as e:
                last_e = e
                count += 1
                pass
            # end try
        # end while

        # Check for error
        if not success:
            raise PageParserRetrievalError(u"Can't retrieve HTML page after {} tries : {}".format(count, last_e))
        # end if

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
        self._title, self._raw_title = self._extract_title(data)
        self._text = self._extract_text(data)
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
        raw_title = soup.title.string.strip()
        new_title = unicode(raw_title)
        new_title = new_title.replace(u'\n', u'').replace(u'\t', u'').replace(u"'", u"\'").replace(u"&amp;",
                                                                                                   u"&").replace(u'\r',
                                                                                                                 u'')
        new_title = new_title.replace(u'â&euro;&trade;', u"\'").replace(u'&#8217;', u"\'").replace(u'&#39;',
                                                                                                   u"\'").replace(
            u'&#039;', u"\'")
        new_title = new_title.replace(u'&#x27;', u'\\').replace(u'&rsquo;', u"\'").replace(u"  ", u" ")
        new_title = pars.unescape(new_title)

        # Return
        return new_title, raw_title
    # end _extract_title

    # Get text
    def _extract_text(self, data):
        """
        Get text from URL
        :return:
        """
        # Soup HTML
        soup = BeautifulSoup(data, "lxml")

        # Total text
        html_text = u""

        # Get each tag
        for tag in ['h1', 'h2', 'h3', 'h4', 'p']:
            # Find all occurencies
            for html_tag in soup.find_all(tag):
                html_text += html_tag.text + u". "
                # end for
        # end for

        # Remove tab
        html_text = html_text.replace(u"\t", u" ")
        html_text = html_text.replace(u"\n", u" ")

        # Remove multiple spaces
        for i in range(20):
            html_text = html_text.replace(u"  ", u" ")
        # end for

        return html_text
    # end get_text

# end PageParser
