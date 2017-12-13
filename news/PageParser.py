#!/usr/bin/python
# -*- coding: utf-8 -*-
#

# Import
import socket
import sys
import urllib2
import httplib
from bs4 import BeautifulSoup


# Can't retrieve page
class PageParserRetrievalError(Exception):
    """
    Exception
    """
    pass
# end PageParserRetrievalError


#
# This is a class to retrieve text from HTML page given an URL.
#
class PageParser(object):
    """
    This is a class to retrieve text from HTML page given an URL.
    """

    # Get text
    @staticmethod
    def get_text(url):
        """
        Get text from URL
        :param url:
        :return:
        """
        # Tries count
        count = 0
        success = False

        # Try
        while count < 10:
            # Get title
            try:
                soup = BeautifulSoup(urllib2.urlopen(url.encode('ascii', errors='ignore')), "lxml")
                success = True
                break
            except urllib2.HTTPError as e:
                raise PageParserRetrievalError(u"HTTP error while retrieving {} : {}\n".format(url, e))
            except socket.error as e:
                count += 1
                pass
            except urllib2.URLError:
                count += 1
                pass
            except httplib.IncompleteRead:
                count += 1
                pass
            except httplib.BadStatusLine:
                count += 1
                pass
            # end try
        # end while

        # Check for error
        if not success:
            raise PageParserRetrievalError(u"Can't retrieve HTML page after {} tries".format(count))
        # end if

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
