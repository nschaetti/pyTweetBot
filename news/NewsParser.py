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
                    if ("http://" in attr[1] or "https://" in attr[1]) and "google." not in attr[1] and "youtube" not \
                            in attr[1] and "blogger.com" not in attr[1]:
                        # URL
                        url = attr[1]

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
        return self.news
    # end get_news

# end NewsParser
