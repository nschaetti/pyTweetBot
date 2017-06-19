#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup
import numpy as np
import time
import random


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

        # Init
        try:
            self.news
        except:
            self.news = []
            pass

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
    def getNews(self):
        return self.news
    # end getNews

# end getNews


#
# This is a Google News client
# Which return an array containing the urls and titles
#
class GoogleNewsClient(object):

    # constructor
    def __init__(self, keyword, lang, country):
        # Parameters
        self.keyword = keyword
        self.lang = lang
        self.country = country
    # end constructor

    # _getNewsTitle
    def getNewsTitle(self,url):

        # HTML parser
        pars = HTMLParser()

        # Get URL's content
        soup = BeautifulSoup(urllib2.urlopen(url,timeout=10000))

        # Clean strange characters
        new_title = unicode(soup.title.string.strip())
        new_title = new_title.replace(u'\n',u'').replace(u'\t',u'').replace(u"'",u"\'").replace(u"&amp;",u"&").replace(u'\r',u'')
        new_title = new_title.replace(u'â&euro;&trade;',u"\'").replace(u'&#8217;',u"\'").replace(u'&#39;',u"\'").replace(u'&#039;',u"\'")
        new_title = new_title.replace(u'&#x27;',u'\\').replace(u'&rsquo;',u"\'").replace(u"  ",u" ")
        new_title = pars.unescape(new_title)

        # Return
        return new_title
    # end _getNewsTitle

    # _getPage(self,url,page)
    def getPage(self,page):
		
		# Init
		news = []
		
		# Call URL
		headers = { 'User-Agent' : "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3" }
		request = urllib2.Request("https://www.google.ch/search?hl=" + self.lang + "&gl=" + self.country + "&q=" + self.keyword.replace(" ","+") + "&tbm=nws&start=" + str(page*10), None, headers)
		html = urllib2.urlopen(request,timeout=5).read()
		
		# instantiate the parser and fed it some HTML
		parser = NewsParser()
		parser.feed(html)
		urls = parser.getNews()
		
		# For each url
		for url in urls:
			
			# Get title
			try:
				title = self.getNewsTitle(url)
				news.append((url,title))
			except urllib2.HTTPError:
				continue
			except:
				continue
		
		return news
	
	# getNews
	def getNews(self, start = 0, end = 0):
		
		# Init
		news = []
		
		# For each page
		for page in np.arange(start,end+1):
			
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Getting page ' + str(page)
			
			# Add page's news
			try:
				news += self.getPage(page)
			except:
				continue
			
			# Wait for random time
			time.sleep(random.randint(15,35))
		
		# return
		return news
		
	#end getNews

##########################################################################
# MAIN
##########################################################################

# Main function
"""if __name__ == "__main__":
	
	# New Google News client
	client = GoogleNewsClient("machine learning","fr","fr_ch")
	news = client.getNews(start = 0, end = 2)
	for new in news:
		print "#" + new[1] + "# " + new[0]"""
