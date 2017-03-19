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

##########################################################################
# MAIN
##########################################################################

def checkTweet(keywords, tweet, json_data):
	
	ok = False
	
	for keyword in keywords:
		
		# Normal
		ok = ok or keyword in tweet.text
		ok = ok or keyword.lower() in tweet.text.lower()
		ok = ok or keyword.capitalize() in tweet.text.capitalize()
		ok = ok or keyword.title() in tweet.text.title()
		ok = ok or keyword.upper() in tweet.text.upper()
		
		# Without space
		ok = ok or keyword.replace(" ","") in tweet.text
		ok = ok or keyword.lower().replace(" ","") in tweet.text.lower()
		ok = ok or keyword.capitalize().replace(" ","") in tweet.text.capitalize()
		ok = ok or keyword.title().replace(" ","") in tweet.text.title()
		ok = ok or keyword.upper().replace(" ","") in tweet.text.upper()
		
		# Barre
		ok = ok or keyword.replace(" ","-") in tweet.text
		ok = ok or keyword.lower().replace(" ","-") in tweet.text.lower()
		ok = ok or keyword.capitalize().replace(" ","-") in tweet.text.capitalize()
		ok = ok or keyword.title().replace(" ","-") in tweet.text.title()
		ok = ok or keyword.upper().replace(" ","-") in tweet.text.upper()
	
	# No retweet
	ok = ok and not "RT @" in tweet.text
	
	# Limit
	if ok and random.random() <= float(json_data["retweet"]["limit_prob"]):
		# Random
		if ok and random.random() <= float(json_data["retweet"]["retweet_prob"]):
			return "retweet"
		elif ok:
			return "like"
	return ""
#end checkTweet

def retweetExists(tweet):
	
	# No '
	ttext = tweet.text
	if ttext.find(u"http") != -1:
		ttext = ttext[:ttext.find(u"http")]
	if ttext.find(u"//www") != -1:
		ttext = ttext[:ttext.find(u"//www")]
	ttext = ttext.replace(u"'",u"\\'")
	
	# Command
	command = u"SELECT * FROM planed_actions WHERE value1 like '" + str(tweet.id) + u"' or value2 like '" + ttext + "'"
	
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
#end retweetExists

def censureChecker(new_title, exclude):
	ok = True
	
	for ex in exclude:
		if ex in new_title:
			ok = False
			break
	
	return ok
#end censureChecker

def alreadyRetweeted(tweet):
	
	# No '
	ttext = tweet.text
	if ttext.find(u"http") != -1:
		ttext = ttext[:ttext.find(u"http")]
	if ttext.find(u"//www") != -1:
		ttext = ttext[:ttext.find(u"//www")]
	ttext = ttext.replace(u"'",u"\\'")
	
	# Command
	command = u"SELECT * FROM tweets WHERE new_url like '" + ttext + "'"
	
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
#end alreadyRetweeted

def insertRetweet(con, rtid, text, temp_time, action):
	
	# No '
	if text.find(u"http") != -1:
		text = text[:text.find(u"http")]
	if text.find(u"//www") != -1:
		text = text[:text.find(u"//www")]
	text = text.replace(u"'",u"\\'")
	text = text.replace(u"'",u"\\'")
	text = text.replace(u"\"",u"\\\"")
	text = text.replace(u"…",u"")
	
	# Insert
	try:
		command = u"INSERT INTO planed_actions (id,type,value1,value2,date) VALUES (0,'" + action + "',\"" + unicode(str(rtid)) + u"\",\"" + unicode(text) + u"\",'" + unicode(str(temp_time)) + u"')"
		cur = con.cursor()
		cur.execute(command.encode(sys.stdout.encoding))
		con.commit()
	except:
		pass
	
#end insertRetweet

def timelineRetweet(api, con, json_data, how_many):
	
	count = 0
	print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Research potential retweets in timeline'
	
	# Keywords
	keywords = json_data["retweet"]["keywords"]
	nb_pages = json_data["retweet"]["nbpages"]
	
	# Search
	limit = 0
	c = tweepy.Cursor(api.home_timeline).pages(limit = nb_pages)
	
	while True:
		
		# Page
		try:
			page = c.next()
		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
		
		# For each tweet in the page
		for tweet in page:
			
			if not retweetExists(tweet) and not alreadyRetweeted(tweet) and censureChecker(tweet.text, json_data["news_settings"]["exclude"]):
				action = checkTweet(keywords, tweet, json_data)
				if action == "retweet" or action == "like":
					print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Will ' + action + ' ' + tweet.text
					
					# Time
					temp_time = time.time() + random.randint(0,86400*int(json_data["news_settings"]["interval_days"]))
					
					# Insert
					insertRetweet(con, tweet.id, tweet.text, temp_time, action = action)
					count += 1
					if count >= how_many:
						return
			
		
		# Mind the limits
		#print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Waiting before next page...'
		time.sleep(60)
		limit += 1
		if limit > nb_pages:
			break
#end timelineRetweet

def searchRetweet(api, con, json_data, keyword, how_many):
	
	count = 0
	print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Research potential retweets in keyword ' + keyword
	
	# Keywords
	nb_pages = json_data["retweet"]["nbpages"]
	
	# Search
	limit = 0
	c = tweepy.Cursor(api.search, q=keyword).pages(limit = nb_pages)
	
	while True:
		
		# Page
		try:
			page = c.next()
		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
		
		# For each tweet in the page
		for tweet in page:
			
			if not retweetExists(tweet) and not alreadyRetweeted(tweet) and censureChecker(tweet.text, json_data["news_settings"]["exclude"]):
				action = checkTweet(keywords, tweet, json_data)
				#print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Will ' + action + ' ' + tweet.text
				if action == "retweet" or action == "like":
					print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] Will ' + action + ' ' + tweet.text
					
					# Time
					temp_time = time.time() + random.randint(0,86400*int(json_data["news_settings"]["interval_days"]))
					
					# Insert
					insertRetweet(con, tweet.id, tweet.text, temp_time, action = action)
					count += 1
					if count >= how_many:
						return
		
		# Mind the limits
		time.sleep(60)
		limit += 1
		if limit > nb_pages:
			break
	
#end searchRetweet

def deleteDoublons(con):
	
	# Insert
	command = u"DELETE t1 FROM planed_actions AS t1, planed_actions AS t2 WHERE t1.type like 'retweet' and t2.type like 'retweet' and t1.id > t2.id AND t1.value2 = t2.value2"
	cur = con.cursor()
	cur.execute(command.encode(sys.stdout.encoding))
	con.commit()
	
#end deleteDoublons

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
	
	# Keywords
	keywords = json_data["retweet"]["keywords"]
	nb_pages = json_data["retweet"]["nbpages"]
	how_many = json_data["retweet"]["count"]
	
	# Search
	for keyword in keywords:
		searchRetweet(api, con, json_data, keyword, how_many / 2.0)
	
	# Timeline
	timelineRetweet(api, con, json_data, how_many / 2.0)
	
	# Delete doublons
	deleteDoublons(con)
