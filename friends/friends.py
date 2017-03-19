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

# For each followers
"""for friend in user.followers():

	# Check if in data base
	cur = con.cursor()
	cur.execute("SELECT * FROM friends WHERE screen_name like '" + friend.screen_name + "'")
	rows = cur.fetchall()
	
	# Exists or not
	if len(rows) == 0:
		cur.execute("INSERT INTO friends (screen_name,direction,date) VALUES ('" + friend.screen_name + "','in'," + str(time.time()) + ")")
		con.commit()
	else:
		cur.execute("UPDATE friends SET direction = 'in' WHERE screen_name like '" + friend.screen_name + "'")"""

# Insert statistics
def insertStatistics(api, con, user):
	
	# Check if in database
	cur = con.cursor()
	
	# Insert
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Inserting statistics..."
	cur.execute("INSERT INTO statistics (friends_count,followers_count,statuses_count) VALUES (" + str(user.friends_count) + "," + str(user.followers_count) + "," + str(user.statuses_count) + ")")
	con.commit()

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
				#sendDirectMessage(api, follower, json_data)
			else:
				print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Updating " + follower.screen_name
				cur.execute("UPDATE friends SET direction = 'in', friends_count = " + str(follower.friends_count) + ", followers_count = " + str(follower.followers_count) + ", statuses_count = " + str(follower.statuses_count) + ", day = " + str(day_num) + " WHERE screen_name like '" + follower.screen_name + "'")
				con.commit()
		time.sleep(60)
# end updateFollowers

# Update all friends
def updateFriends(api, con, user, day_num):
	
	# Iterate through page
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Updating friends..."
	for page in tweepy.Cursor(api.friends).pages():
		# For each follower in the page
		for friend in page:
			# Check if in database
			cur = con.cursor()
			cur.execute("SELECT * FROM friends WHERE screen_name like '" + friend.screen_name + "'")
			rows = cur.fetchall()

			# Exists or not
			if len(rows) == 0:
				print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Inserting " + friend.screen_name
				
				# Insert in database
				cur.execute("INSERT INTO friends (screen_name,direction,friends_count,followers_count,statuses_count,date,day) VALUES ('" + friend.screen_name + "','out'," + str(friend.friends_count) + "," + str(friend.followers_count) + "," + str(friend.statuses_count) + "," + str(time.time()) + "," + str(day_num) + ")")
				con.commit()
			else:
				print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Updating " + friend.screen_name
				if rows[0][2] == 'in':
					cur.execute("UPDATE friends SET direction = 'both', friends_count = " + str(friend.friends_count) + ", followers_count = " + str(friend.followers_count) + ", statuses_count = " + str(friend.statuses_count) + ", day = " + str(day_num) + " WHERE screen_name like '" + friend.screen_name + "'")
				else:
					cur.execute("UPDATE friends SET direction = 'out', friends_count = " + str(friend.friends_count) + ", followers_count = " + str(friend.followers_count) + ", statuses_count = " + str(friend.statuses_count) + ", day = " + str(day_num) + " WHERE screen_name like '" + friend.screen_name + "'")
				con.commit()
		time.sleep(60)
# end updateFriends

# Delete oldies
def deleteOldies(api, con, day_num):
	
	# Delete
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Deleting oldies..."
	cur = con.cursor()
	cur.execute("DELETE FROM friends WHERE direction NOT LIKE 'none' AND day <> " + str(day_num))
	con.commit()
# end deleteOldies

# Select unfollow
def selectUnfollow(api, con, user, json_data):
	
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Selecting user to unfollow..."
	
	# Params
	unfollow_count = int(json_data["friends"]["new_unfollow"])
	unfollow_time = int(json_data["friends"]["unfollow_interval"])

	# Select
	cur = con.cursor()
	cur.execute("SELECT * FROM `friends` WHERE `direction` like 'out' and `followers_count` < 40000 and `special` = 0 and UNIX_TIMESTAMP()-`date` >= " + str(unfollow_time) + " LIMIT " + str(unfollow_count))
	rows = cur.fetchall()
	
	# For each row
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + str(len(rows)) + " user to unfollow..."
	for row in rows:
		
		# Info
		screen_name = row[1]
		# Check if already exists
		cur.execute("SELECT * FROM `planed_actions` WHERE value1 like '" + screen_name + "' and type like 'unfollow'")
		rows2 = cur.fetchall()
		
		if len(rows2) == 0:
			# Time
			temp_time = time.time() + random.randint(0,604800)
			
			# Insert
			cur.execute("INSERT INTO planed_actions (type,value1,date) VALUES ('unfollow','" + screen_name + "'," + str(temp_time) + ")")
			con.commit()

# Follow back
def followBack(api, con, user):
	
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Following back..."
	
	# Select
	cur = con.cursor()
	cur.execute("SELECT * FROM `friends` WHERE direction like 'in'")
	rows = cur.fetchall()
	
	# For each row
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + str(len(rows)) + " user to follow back..."
	for row in rows:
		
		# Info
		screen_name = row[1]
		
		# Check if already exists
		cur.execute("SELECT * FROM `planed_actions` WHERE value1 like '" + screen_name + "' and type like 'follow'")
		rows2 = cur.fetchall()
		
		if len(rows2) == 0:
			# Time
			temp_time = time.time() + random.randint(0,604800)
			
			# Insert
			cur.execute("INSERT INTO planed_actions (type,value1,date) VALUES ('follow','" + screen_name + "'," + str(temp_time) + ")")
			con.commit()

# Follow new people
def followNewPeople(api, con, user, json_data):
	
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "Selecting new people to follow..."
	
	# Params
	new_count = int(json_data["friends"]["new_followers"])
	print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + str(new_count) + " new friends to follow..."

	# Select
	cur = con.cursor()
	cur.execute("SELECT * FROM `friends` WHERE `direction` like 'in' or `direction` like 'both'")
	rows = cur.fetchall()
	rows = list(rows)
	
	# Shuffle randomly
	print rows[0]
	random.shuffle(rows)
	print rows[0]
	
	# Fow each follower
	count = 0
	for row in rows:
		
		# Get user
		print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "\tSearching through " + row[1] + " followers..."
		follower = api.get_user(row[1])
		
		# Iterate through page
		for page in tweepy.Cursor(api.friends,screen_name=row[1]).pages():
			
			# For each follower in the page
			for friend in page:
				if count < new_count:
					if friend.friends_count != 0 and friend.followers_count / friend.friends_count <= 1.2 and friend.statuses_count > 100:
						
						# Check if already exists
						cur.execute("SELECT * FROM `planed_actions` WHERE value1 like '" + friend.screen_name + "' and type like 'follow'")
						rows2 = cur.fetchall()
						
						# Check if in database
						cur.execute("SELECT * FROM `friends` WHERE screen_name like '" + friend.screen_name)
						rows3 = cur.fetchall()
						
						if len(rows2) == 0 and len(row2) == 0:
							# Time
							temp_time = time.time() + random.randint(0,604800)
							
							# Insert
							print '[' + time.strftime("%Y-%m-%d %H:%M") + '] ' + "\tWe will follow " + friend.screen_name
							cur.execute("INSERT INTO planed_actions (type,value1,date) VALUES ('follow','" + friend.screen_name + "'," + str(temp_time) + ")")
							con.commit()
							count += 1
				else:
					break
			
			# Check limits
			if count < new_count:
				time.sleep(60)
			else:
				break
		
		# Check limits
		if count < new_count:
			time.sleep(60)
		else:
			break

# Send report
def sendReport(api, user):
	
	# Info
	to = 'n.schaetti@gmail.com'
	gmail_user = 'n.schaetti@gmail.com'
	gmail_pwd = 'juGL8FgASinqH746zWe4'
	
	# Send the message via our own SMTP server, but don't include the
	# envelope header.
	s = smtplib.SMTP("smtp.gmail.com",587)
	s.ehlo()
	s.starttls()
	s.ehlo
	s.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Report from nilsbot \n'
	msg = header + '\n ' + user.followers_count + ' followers, ' + user.friends_count + ' friends, ' + user.statuses_count + ' tweets \n\n'
	s.sendmail(gmail_user, to, msg)
	s.quit()

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
	
	# Save statistics
	insertStatistics(api, con, user)

	# Update followers
	updateFollowers(api, con, user, day_num, json_data)

	# Update friends
	updateFriends(api, con, user, day_num)
	
	# Delete old entries
	deleteOldies(api, con, day_num)
	
	# Select unfollow
	selectUnfollow(api, con, user, json_data)
	
	# Follow back
	followBack(api, con, user)
	
	# Follow new people
	followNewPeople(api, con, user, json_data)
	
	# Send email
	#sendReport(api, user)

# end main


