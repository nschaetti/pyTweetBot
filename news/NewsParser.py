#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : news.NewsParser.py
# Description : Google News client.
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
from HTMLParser import HTMLParser


#
# This is a class parsing HTML from Google news.
# It returns an array containing the URLs.
#
class NewsParser(HTMLParser):
    """
    This is a class parsing HTML from Google news.
    It returns an array containing the URLs.
    """

    # Handle startag
    def handle_starttag(self, tag, attrs):
        """
        Handle startag
        :param tag: Tag to handle
        :param attrs: Tag's attributes
        """
        # Init
        try:
            self.news
        except:
            self.news = []
            pass
        # end if

        # We're searching a tags
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    if ("http://" in attr[1] or "https://" in attr[1]) and "google." not in attr[1] and "youtube" not \
                            in attr[1] and "blogger.com" not in attr[1]:
                        # URL
                        url = attr[1]

                        # URL
                        if url[:7] == u"/url?q=":
                            url = url[7:]
                        # end if

                        # No URL options
                        url = url[:url.find(u'%')] if url.find(u'%') != -1 else url
                        url = url[:url.find(u'&')] if url.find(u'&') != -1 else url

                        # Substring
                        if url not in self.news:
                            self.news.append(url)
                        # end if
                    # end if
                # end if
            # end for
        # end if
    # end handle_starttag

    # Get news
    def get_news(self):
        """
        Get the news
        :return:
        """
        return self.news
    # end get_news

# end NewsParser
