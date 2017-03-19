#!/usr/bin/python
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import urllib2
import simplejson
import sys
import numpy as np
from BeautifulSoup import BeautifulSoup
import socket
import time
import random
import argparse
import json
import tweepy
from string import printable
import HTMLParser
from httplib import IncompleteRead
from googlenewsclient import GoogleNewsClient

##########################################################################
# FUNCTION
##########################################################################

def checkIfPlanned(new_title, new_url):
	
	command = u"SELECT * FROM planed_actions WHERE value2 like '" + new_url.replace("'","\\'") + u"' OR value1 like '" + new_title.replace("'","\\'") + u"'"
	
	# Check if registered
	cur = con.cursor()
	try:
		cur.execute(command.encode(sys.stdout.encoding))
	except mdb.OperationalError as err:
		return False
	except:
		return True
		pass
	rows = cur.fetchall()
	
	# If not already registered
	if len(rows) == 0:
		return False
	else:
		return True

def checkIfTweeted(new_title, new_url):
	
	command = u"SELECT * FROM tweets WHERE new_url like '" + new_url + u"' OR new_title like '" + new_title + u"'"
	
	# Check if registered
	cur = con.cursor()
	try:
		cur.execute(command.encode(sys.stdout.encoding))
	except mdb.OperationalError as err:
		return False
	rows = cur.fetchall()
	
	# If not already registered
	if len(rows) == 0:
		return False
	else:
		return True

def deleteDoublons(con):
	
	# Insert
	command = u"DELETE t1 FROM planed_actions AS t1, planed_actions AS t2 WHERE t1.id > t2.id AND t1.value1 = t2.value1"
	cur = con.cursor()
	cur.execute(command.encode(sys.stdout.encoding))
	con.commit()
	
#end deleteDoublons

def censureChecker(new_title, exclude):
	ok = True
	
	for ex in exclude:
		if ex in new_title:
			ok = False
			break
	
	return ok
#end censureChecker

##########################################################################
# MAIN
##########################################################################

# Main function
if __name__ == "__main__":
	
	# Arguments
	parser = argparse.ArgumentParser(prog='friends', description='NilsBot Friends', epilog='Seulement pour mon usage')
	parser.add_argument('--configfile', help='Fichier de configuration')
	args = parser.parse_args()
	
	# Open config file
	json_file = open(args.configfile)
	json_data = json.load(json_file)
	
	# Auth to Twitter
	auth = tweepy.OAuthHandler(json_data['twitter']['auth_token1'],json_data['twitter']['auth_token2'])
	auth.set_access_token(json_data['twitter']['access_token1'],json_data['twitter']['access_token2'])
	api = tweepy.API(auth)
	
	# Try connection to MySQL database
	try:
		con = mdb.connect(json_data['database']['host'], json_data['database']['username'], json_data['database']['password'], json_data['database']['database'], charset='utf8');
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	
	# For each keywords
	for news_rules in json_data["news"]:
		
		# Keyword to search and hashtag
		keyword = unicode(news_rules["keyword"])
		hashtag = unicode("#" + keyword.replace(' ','').replace('-',''))
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Researching for ' + keyword
		
		# For each countries
		for ned in news_rules["countries"]: 
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Country ' + ned
			
			# For each langs
			for lang in news_rules["languages"]:
				print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Language ' + lang
				
				# New Google News client
				print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Getting news...'
				client = GoogleNewsClient(keyword,lang,ned)
				news = client.getNews(start = 0, end = 20)
				
				# For each news
				for new in news:
					
					# Title and url
					new_title = new[1].replace("\'","\\'").replace('"','\\"').replace(u"«","\\'").replace(u"»","\\'")
					new_url = new[0]
					
					# No ...
					if "..." not in new_title and len(new_title) < (140 - 26 - 1):
						if "not" not in news_rules or news_rules["not"] not in new_title:
							if u"έ" not in new_title and u"ě" not in new_title and u"ה" not in new_title:
								if censureChecker(new_title, json_data["news_settings"]["exclude"]):
									
									# Replace the hastag in the title
									new_title = new_title.replace(keyword,hashtag).replace(keyword.title(),hashtag).replace(keyword.replace(' ','-'),hashtag).replace(keyword.replace(' ','-').title(),hashtag).replace(keyword.capitalize(),hashtag)
									new_title = new_title.replace("##","#").replace("###","#").replace("####","#")
									
									# Add hashtags
									new_title += "."
									for htag in news_rules["hashtags"]:
										if len(new_title + u" " + unicode(htag)) < (140 - 26):
											new_title += u" " + unicode(htag)
									
									# Check
									if not checkIfPlanned(new_title,new_url) and not checkIfTweeted(new_title,new_url):
										print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + new_title + u" " + new_url
										
										# Time
										temp_time = time.time() + random.randint(0,86400*int(json_data["news_settings"]["interval_days"]))
										
										# Insert
										try:
											command = u"INSERT INTO planed_actions (id,type,value1,value2,value3,date) VALUES(0,'tweet',\"" + new_title + u"\",'" + new_url + u"',''," + unicode(str(temp_time)) + u")"
											cur = con.cursor()
											cur.execute(command.encode(sys.stdout.encoding))
											con.commit()
										except:
											print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + "Error encoding command..."
											pass
			
			# Wait for random time
			time.sleep(random.randint(30,60))
		
		# Wait for random time
		time.sleep(random.randint(60,240))
	
	# Delete doublons
	deleteDoublons(con)
	
	if con:
		con.close()

