#!/usr/bin/python
# -*-coding:Utf-8 -*
import tweepy
import time
import MySQLdb as mdb
import datetime
import smtplib
import random
import numpy as np
import argparse
import json

def sendDirectMessage(api, follower, json_data):
	
	print u'[' + time.strftime("%Y-%m-%d %H:%M") + u'] ' + u"Sending direct message to " + unicode(follower.screen_name)
	
	# Send direct message
	try:
		api.send_direct_message(user_id = follower.id, text = json_data["direct_message"])
		time.sleep(60)
	except:
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] \033[91m' + u"Limit reached, waiting 15 minutes... " + '\033[0m'
		time.sleep(900)

# Update all the followers
def updateFollowers(api, con, user, day_num, json_data):
	
	# Only iterate through pages
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Updating followers..."
	for page in tweepy.Cursor(api.followers).pages():
		# For each follower in the page
		for follower in page:
			#print follower
			# Check if in data base
			cur = con.cursor()
			cur.execute("SELECT * FROM friends WHERE screen_name like '" + follower.screen_name + "'")
			rows = cur.fetchall()
			
			# Exists or not
			if len(rows) == 0:
				print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Inserting " + follower.screen_name
				
				# Insert
				cur.execute("INSERT INTO friends (screen_name,direction,friends_count,followers_count,statuses_count,date,day) VALUES ('" + follower.screen_name + "','in'," + str(follower.friends_count) + "," + str(follower.followers_count) + "," + str(follower.statuses_count) + "," + str(time.time()) + "," + str(day_num) + ")")
				con.commit()
				
				# Send direct message
				sendDirectMessage(api, follower, json_data)
			else:
				print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Updating " + follower.screen_name
				cur.execute("UPDATE friends SET direction = 'in', friends_count = " + str(follower.friends_count) + ", followers_count = " + str(follower.followers_count) + ", statuses_count = " + str(follower.statuses_count) + ", day = " + str(day_num) + " WHERE screen_name like '" + follower.screen_name + "'")
				con.commit()
		time.sleep(60)
# end updateFollowers

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

	# Connection to MySQL
	try:
		print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Trying to connect to MYSQL database..."
		con = mdb.connect(json_data['database']['host'], json_data['database']['username'], json_data['database']['password'], json_data['database']['database'], charset='utf8');
	except mdb.Error, e:
		print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	
	# Number of the day
	day_num = datetime.datetime.today().day + datetime.datetime.today().month * 100 + datetime.datetime.today().year * 10000
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Day num : " + str(day_num)
	
	# Get user
	user = api.get_user(json_data['twitter']['user'])
	
	# Update followers
	updateFollowers(api, con, user, day_num, json_data)
	
# end main


