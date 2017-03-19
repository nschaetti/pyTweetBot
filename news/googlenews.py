#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib2
import re
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

##########################################################################
# CLASSES
##########################################################################

#
# This is a class parsing HTML from Google news.
# It returns an array containing the URLs.
#
class NewsParser(HTMLParser):
	
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
	#end handle_starttag
	
	# getNews
	def getNews(self):
		return self.news

#
# This is a Google News client
# Which return an array containing the urls and titles
#
class GoogleNewsClient():
	
	# constructor
	def __init__(self, keyword, lang, country):
		# Parameters
		self.keyword = keyword
		self.lang = lang
		self.country = country
	#end constructor
	
	# _getNewsTitle
	def _getNewsTitle(self,url):
		
		# HTML parser
		pars = HTMLParser()
		
		# Get URL's content
		soup = BeautifulSoup(urllib2.urlopen(url,timeout=5000))
		
		# Clean strange characters
		new_title = unicode(soup.title.string.strip())
		new_title = new_title.replace(u'\n',u'').replace(u'\t',u'').replace(u"'",u"\\'").replace(u"&amp;",u"&")
		new_title = new_title.replace(u'â&euro;&trade;',u"\\'").replace(u'&#8217;',u"\\'").replace(u'&#39;',u"\\'").replace(u'&#039;',u"\\'")
		new_title = new_title.replace(u'&#x27;',u'\\').replace(u'&rsquo;',u"\\'").replace(u"  ",u" ")
		new_title = pars.unescape(new_title)
		
		# Return
		return new_title
		
	#end _getNewsTitle
	
	# getNews
	def getNews(self):
		
		# Init
		news = []
		
		# Call URL
		headers = { 'User-Agent' : "Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3" }
		request = urllib2.Request("https://www.google.ch/search?hl=" + self.lang + "&gl=" + self.country + "&q=" + self.keyword.replace(" ","+") + "&tbm=nws", None, headers)
		html = urllib2.urlopen(request).read()
		
		# instantiate the parser and fed it some HTML
		parser = NewsParser()
		parser.feed(html)
		urls = parser.getNews()
		
		# For each url
		for url in urls:
			
			# Get title
			try:
				title = self._getNewsTitle(url)
				news.append((url,title))
			except urllib2.HTTPError:
				continue
		
		return news
		
	#end getNews

##########################################################################
# MAIN
##########################################################################

# Main function
if __name__ == "__main__":
	
	# New Google News client
	client = GoogleNewsClient("machine learning","en","us")
	print client.getNews()
