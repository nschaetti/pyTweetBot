#!/usr/bin/python
# -*- coding: utf-8 -*-
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

    # handle_starttag
    def handle_starttag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        :return:
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
                    if "/url?q=" in attr[1]:
                        # URL
                        url = attr[1]

                        # Substring
                        self.news.append(url[url.find("http"):url.rfind("&sa=")])
                    # end if
                # end if
            # end for
        # end if
    # end handle_starttag

    # Get news
    def get_news(self):
        return self.news
    # end get_news

# end NewsParser
