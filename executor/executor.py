#!/usr/bin/python
# -*-coding:Utf-8 -*
import tweepy
import time
import MySQLdb as mdb
import datetime
import argparse
import json
import sys

# Tweet limit reached ?
in_limit = True

# Delete an action
def deleteAction(api, con, action_id, action_value1, err):
	
	# Cursor
	cur = con.cursor()
	
	# Delete
	if err:
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] \033[91m' + u"Deleting action " + action_value1 + " because errors" + '\033[0m'
	else:
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] \033[94m' + u"Deleting action " + action_value1 + '\033[0m'
	cur.execute("DELETE FROM planed_actions WHERE id = " + str(action_id))
	con.commit()

# Execute an action
def executeAction(api, con, row):
	
	global in_limit
	
	# Infos
	action_id = row[0]
	action_type = row[1]
	action_value1 = unicode(row[2])
	action_value2 = unicode(row[3])
	action_value3 = unicode(row[4])
	action_date = row[5]

	# Cursor
	cur = con.cursor()

	try:	
		# Type
		if action_type == "follow":
			
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Following \033[94m" + unicode(action_value1) + u'\033[0m'
			api.create_friendship(action_value1)
			
		elif action_type == "unfollow":
			
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Unfollowing \033[94m" + unicode(action_value1) + u'\033[0m'
			api.destroy_friendship(action_value1)
			
			# Put this person in noman's land
			command = u"UPDATE friends SET direction = 'none' WHERE screen_name like '" + unicode(action_value1) + u"'"
			cur.execute(command.encode(sys.stdout.encoding))
			con.commit()
			
		elif action_type == "tweet" and in_limit == True:
			print unicode(action_value1)	
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Tweeting \033[94m" + unicode(action_value1) + u" " + unicode(action_value2) + u'\033[0m'
			tweet = action_value1 + u" " + action_value2
			api.update_status (status = tweet)
			
			# Put this as tweeted
			command = u"INSERT INTO tweets (new_title,new_url) VALUES ('" + unicode(action_value1.replace("'","\\'")) + u"','" + unicode(action_value2.replace("'","\\'")) + u"')"
			cur.execute(command.encode(sys.stdout.encoding))
			con.commit()
			
		elif action_type == "retweet":
			
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Retweeting \033[94m" + unicode(action_value1) + u'\033[0m'
			tweet_id = int(action_value1)
			api.retweet(tweet_id)
			
			# Put this as tweeted
			command = u"INSERT INTO tweets (new_title,new_url) VALUES ('" + unicode(action_value1.replace(u"'",u"\'").replace(u'"',u'\"')) + u"','" + unicode(action_value2.replace(u"'",u"\'").replace(u'"',u'\"')) + u"')"
			#print command
			cur.execute(command.encode(sys.stdout.encoding))
			con.commit()
		
		elif action_type == "like":
			
			print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Liking \033[94m" + unicode(action_value1) + u'\033[0m'
			tweet_id = int(action_value1)
			api.create_favorite(tweet_id)
			
			# Put this as tweeted
			command = u"INSERT INTO tweets (new_title,new_url) VALUES ('" + unicode(action_value1.replace(u"'",u"\'").replace(u'"',u'\"')) + u"','" + unicode(action_value2.replace(u"'",u"\'").replace(u'"',u'\"')) + u"')"
			cur.execute(command.encode(sys.stdout.encoding))
			con.commit()
			
	except tweepy.error.TweepError as err:
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] \033[91m' + u"Can't execute action " + str(action_id) + u'\033[0m'
		if type(err[0][0]) is str:
			if "429" in err[0]:
				print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u" Limit exceeded.. exit"
				in_limit = False
				exit()
		else:
			if err[0][0]['code'] in [160,108,186,327,328,144,187,158]:
				#print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u"Deleting action " + action_value1 + " because errors"
				deleteAction(api, con, action_id, action_value1, True)
			elif err[0][0]['code'] == 185:
				print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u" Limit exceeded.. exit"
				in_limit = False
				exit()
			else:
				print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] ' + u'\033[91m' + str(err) + u'\033[0m'
				deleteAction(api, con, action_id, action_value1, True)
		pass
	except UnicodeEncodeError as err:
		
		# Log
		print u'[' + unicode(time.strftime("%Y-%m-%d %H:%M")) + u'] \033[91m' + u"Encoding error for " + str(action_id) + u'\033[0m'

		# Delete it	
		deleteAction(api, con, action_id, "", False)
		
		pass
	else:
		deleteAction(api, con, action_id, action_value1, False)

# Get actions
def getActions(api, con, action_type, limit):
	
	# Select
	command = u"SELECT * FROM `planed_actions` WHERE type like '" + action_type + "' ORDER BY date LIMIT " + str(limit)
	cur = con.cursor()
	cur.execute(command.encode(sys.stdout.encoding))
	rows = cur.fetchall()
	
	return rows
	
# Get actions
def getActionsOR(api, con, action_type1, action_type2, limit):
	
	# Select
	command = u"SELECT * FROM `planed_actions` WHERE type like '" + action_type1 + "' OR type like '" + action_type2 + "' ORDER BY date LIMIT " + str(limit)
	cur = con.cursor()
	cur.execute(command.encode(sys.stdout.encoding))
	rows = cur.fetchall()
	
	return rows

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
	
	# Get user
	user = api.get_user(json_data['twitter']['user'])
	
	# Connection to MySQL
	try:
		print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Trying to connect to MYSQL database..."
		con = mdb.connect(json_data['database']['host'], json_data['database']['username'], json_data['database']['password'], json_data['database']['database'], charset='utf8');
	except mdb.Error, e:
		print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	
	# Select
	actions = []
	trys = 0
	while(len(actions) != 8):
		
		# Tweet
		actions = actions + list(getActions(api, con, 'tweet', 2))
		
		# Retweet
		actions = actions + list(getActions(api, con, 'retweet', 1))
		
		# Follow
		actions = actions + list(getActionsOR(api, con, 'follow', 'unfollow', 1))
		
		# Like
		actions = actions + list(getActions(api, con, 'like', 1))
		
		# No infinite loop
		trys += 1
		if trys >= 10:
			break
	
	# For each actions
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] \033[94m' +  str(len(actions)) + " to execute...\033[0m"
	count = 0
	for row in actions:
		executeAction(api, con, row)
		count += 1
		if count >= 8:
			exit()
