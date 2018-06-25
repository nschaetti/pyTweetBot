<p align="center"><img src="docs/images/pytweetbot.png" /></p>

--------------------------------------------------------------------------------
A Twitter bot and library written in Python to replace yourself, search and publish news about specific subjects on Twitter, and automatize content publishing.

<a href="https://twitter.com/intent/tweet?text=pyTweetBot%20is%20A%20Twitter%20bot%20written%20in%20Python%20to%20replace%20yourself,%20search%20and%20publish%20news%20about%20specific%20subjects%20on%20Twitter&url=https://github.com/nschaetti/pyTweetBot&hashtags=pytweetbot,twitter,python">
    <img style='vertical-align: text-bottom !important;' src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social" alt="Tweet">
</a>

Join our community to create datasets and deep-learning models! Chat with us on [Gitter](https://gitter.im/pyTweetBot/Lobby) and join the [Google Group](https://groups.google.com/forum/#!forum/pytweetbot) to collaborate with us.

[![PyPI version](https://badge.fury.io/py/pyTweetBot.svg)](https://badge.fury.io/py/pyTweetBot)
[![Documentation Status](https://readthedocs.org/projects/pytweetbot/badge/?version=latest)](https://pytweetbot.readthedocs.io/en/latest/?badge=latest)

This repository consists of:

* pytweetbot.config : Configuration file management;
* pytweetbot.db : MySQL database management;
* pytweetbot.directmessages : Twitter direct message functions;
* pytweetbot.docs : Documentation;
* pytweetbot.executor : Function and objects to execute actions;
* pytweetbot.friends : Function and objects to manage friends and followers;
* pytweetbot.learning : Machine learning functions;
* pytweetbot.mail : Mail functions;
* pytweetbot.news : Manage news acquisition and sources;
* pytweetbot.patterns : Python class patterns;
* pytweetbot.retweet : Manage retweets and sources;
* pytweetbot.stats : Statistics;
* pytweetbot.templates : HTML templates for mail;
* pytweetbot.tools : Tools;
* pytweetbot.tweet : Manage tweets;
* pytweetbot.twitter : Manage access to Twitter;

## Getting started

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.
See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to following package to install pyTweetBot.

* nltk
* argparse
* logging
* tweepy
* sklearn
* pygithub
* brotli
* httplib2
* urlparse2
* HTMLParser
* bs4
* simplejson
* dnspython
* dill
* lxml
* sqlalchemy
* feedparser
* textblob
* numpy
* scipy
* mysql-python

### Installation

    pip install pyTweetBot

## Authors

* **Nils Schaetti** - *Initial work* - [nschaetti](https://github.com/nschaetti/)

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file
for details.

## Configuration

### Configuration file

pyTweetBot takes its configuration in a JSON file which looks as follow :

```javascript
{
	"database" :
	{
		"host" : "",
		"username" : "",
		"password" : "",
		"database" : ""
	},
	"email" : "bot@bot.com",
	"scheduler" :
	{
		"sleep": [6, 13]
	},
	"hashtags":
	[
	],
	"twitter" :
	{
		"auth_token1" : "",
		"auth_token2" : "",
		"access_token1" : "",
		"access_token2" : "",
		"user" : ""
	},
	"friends" :
	{
		"max_new_followers" : 40,
		"max_new_unfollow" : 40,
		"interval" : [15, 60],
		"unfollow_interval" : 604800
	},
	"forbidden_words" :
	[
	],
	"direct_message" : "",
	"tweet" : {
		"max_tweets" : 1800,
		"exclude" : [],
		"interval" : [4.0, 6.0],
		"intervals" : [
			{
				"day": 5,
				"start": 17,
				"end": 23,
				"interval" : [1.0, 3.0]
			}
		]
	},
	"news" :
	[
		{
			"keyword" : "",
			"countries" : ["us","fr"],
			"languages" : ["en","fr"],
			"hashtags" : []
		}
	],
	"rss" :
	[
		{"url" : "http://feeds.feedburner.com/TechCrunch/startups", "hashtags" : "#startups", "lang": ["en"]},
		{"url" : "http://feeds.feedburner.com/TechCrunch/fundings-exits", "hashtags" : "#fundings", "lang": ["en"]}
	],
	"retweet" :
	{
		"max_retweets" : 600,
		"max_likes" : 0,
		"keywords" : [],
		"nbpages" : 40,
		"retweet_prob" : 0.5,
		"limit_prob" : 1.0,
		"interval" : [2.0, 4.0]
	},
	"github" :
	{
		"login": "",
		"password": "",
		"exclude": [],
		"topics" : []
	}
}
```

Their is two required sections :
* Database : contains the information to connect to the MySQL database (host, username, password, database)
* Twitter : contains the information for the Twitter API (auth and access tokens)

### Database configuration

The database part of the configuration file looks like the following

    "database" :
    {
        "host" : "",
        "username" : "",
        "password" : "",
        "database" : ""
    }

This section is mandatory.

### Update e-mail configuration

You can configure your bot to send you an email with the number of new followers in the email section

    "email" : "bot@bot.com"

### Scheduler configuration

The scheduler is responsible for executing the bot's actions and you can configure it the sleep for a specific period
of time.

    "scheduler" :
    {
        "sleep": [6, 13]
    }

Here the scheduler will sleep during 6h00 and 13h00.

### Hashtags

You can add text to be replace as hashtags in your tweet in the "hashtags" section

    "hashtags":
    [
        {"from" : "My Hashtag", "to" : "#MyHashtag", "case_sensitive" : true}
    ]

Here, occurences of "My Hashtag" will be replaced by #MyHashtag.

### Twitter

To access Twitter, pyTweetBot needs four tokens for the Twitter API and your username.

```javascript
"twitter" :
{
    "auth_token1" : "",
    "auth_token2" : "",
    "access_token1" : "",
    "access_token2" : "",
    "user" : ""
}
```

TODO: tutorial to get the tokens

### Friends settings

The friends section has four parameters.

```javascript
"friends" :
{
	"max_new_followers" : 40,
	"max_new_unfollow" : 40,
	"interval" : [15, 60],
	"unfollow_interval" : 604800
}
```

* The max_new_followers set the maximum user that can be followed each day;
* The max_new_unfollow set the maximum user that can be unfollowed each day;
* The interval parameter set the interval in minutes between each follow/unfollow action choosen randomly between the min and the max;

### Create database

You have then to create the database on your MySQL host

    python -m pyTweetBot tools
        --create-database : Create the database structure on the MySQL host
        --export-database : Export tweets, tweeted and followers/friends to a file
        --import-database     Import tweets, tweeted and followers/friends from a file
        --file : File to import / to export to

You can use the "create-database" action for that :

    python -m pyTweetBot tools --config /path/to/config.json --create

It is possible to export bot's data to a file with the export-database command.

    python -m pyTweetBot tools --config /path/to/config.json --export --file export_file.p

And then import the bot's data from the file

    python -m pyTweetBot tools --config /path/to/config.json --import --file export_file.p

## Model training

### Create a dataset

The first step to train a model is to create a dataset of positive and negative examples. This can be done with the
train command and the "dataset" action.

    python -m pyTweetBot train --dataset test.p --config ../nils-config/nilsbot.json --text-size 100 --action dataset --source news

The source argument can take the following value :

* News : URLs from Google News and and RSS streams;
* tweets : Tweets found directly on Twitter;
* friends : Description of Twitter users found directly on Twitter;
* followers : Description of Twitter users found in your list of followers;
* home : Tweets found on our home feed;

### Train a model

Once the dataset is created, we can train a model using the "train" action :

    python -m pyTweetBot train --dataset test.p --config ../nils-config/nilsbot.json --model mymodel.p --action train --text-size 100 --classifier SVM
    INFO:pyTweetBot:Finalizing training...
    INFO:pyTweetBot:Training finished... Saving model to mymodel.p

The classifier parameter can take the following values :

* NaiveBayes : Naive Bayes classifier;
* DecisionTree : Simple decision tree;
* RandomForest : Random forest;
* SVM : Support Vector Machine;

### Test a model

You can test your model's accuracy with the "test" action :

    python -m pyTweetBot train --dataset test.p --config ../nils-config/nilsbot.json --model mymodel.p --action test --text-size 100
    Success rate of 56.1108362197 on dataset

You can now use your model to class tweets.

## Command line

### Launch executors

pyTweetBot launch an executor thread for each action type. You can launch the executor daemon that way :

    python -m pyTweetBot executor --config /etc/bots/bot.conf

### Find new tweets

    python -m pyTweetBot find-tweets --config /etc/bots/bot.conf --model /etc/bots/models/find_tweets.p

### Find new retweets

    python -m pyTweetBot find-retweets --config /etc/bots/bot.conf --model /etc/bots/moedls/find_retweets.p

### Automatise execution with crontab

## Development

### Files

* [pyTweetBot/__main__.py](__main__.py) : Main Python file;
* [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) : Code of conduct for contributors;
* [CONTRIBUTING.md](CONTRIBUTING.md) : Instructions if you want to contribute;
* [pyTweetBot/convert_dataset.py](convert_dataset.py) :
* [pyTweetBot/create_dataset.py](create_dataset.py) :
* [pyTweetBot/direct_messages.py](direct_messages.py) : Send direct messages;
* [Dockerfile](Dockerfile) : Docker configuration file;
* [pyTweetBot/execute_actions.py](execute_actions.py) : Launch the threads to execute actions;
* [pyTweetBot/export_database.py](export_database.py) : Tool functions to export a database;
* [pyTweetBot/find_follows.py](find_follows.py) : Find Twitter users to follow;
* [pyTweetBot/find_github_tweets.py](find_github_tweets.py) : Find tweet about Github activities;
* [pyTweetBot/find_reweets.py](find_retweets.py) : Find posts to retweet;
* [pyTweetBot/find_tweets.py](find_tweets.py) : Find content on the web to tweet;
* [pyTweetBot/find_tweets.py](find_tweets.py) : Python code to find new contents to tweet;
* [pyTweetBot/find_unfollows.py](find_unfollows.py) : Find Twitter users to unfollow;
