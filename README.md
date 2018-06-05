<p align="center"><img src="docs/images/pytweetbot.png" /></p>

--------------------------------------------------------------------------------
A Twitter bot and library written in Python to replace yourself, search and publish news about specific subjects on Twitter, and automatize content publishing.

<a href="https://twitter.com/intent/tweet?text=pyTweetBot%20is%20A%20Twitter%20bot%20written%20in%20Python%20to%20replace%20yourself,%20search%20and%20publish%20news%20about%20specific%20subjects%20on%20Twitter&url=https://github.com/nschaetti/pyTweetBot&hashtags=pytweetbot,twitter,python">
    <img style='vertical-align: text-bottom !important;' src="https://img.shields.io/twitter/url/http/shields.io.svg?style=social" alt="Tweet">
</a>

Join our community to create datasets and deep-learning models! Chat with us on [Gitter](https://gitter.im/EchoTorch/Lobby) and join the [Google Group](https://groups.google.com/forum/#!forum/echotorch/) to collaborate with us.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytweetbot.svg?style=flat-square)
[![Codecov](https://img.shields.io/codecov/c/github/nschaetti/pytweetbot/master.svg?style=flat-square)](https://codecov.io/gh/nschaetti/pyTweetBot)
[![Documentation Status](	https://img.shields.io/readthedocs/pytweetbot/latest.svg?style=flat-square)](http://echotorch.readthedocs.io/en/latest/?badge=latest&style=flat-square)
[![Build Status](https://img.shields.io/travis/nschaetti/pytweetbot/master.svg?style=flat-square)](https://travis-ci.org/nschaetti/pyTweetBot)

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
        "follow_unfollow_ratio_limit" : 1.2,
        "interval" : [30, 45]
    },
    "forbidden_words" :
    [
    ],
    "direct_message" : "",
    "tweet" : {
        "max_tweets" : 1200,
        "exclude" : [],
        "interval" : [2.0, 4.0]
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
        {"url" : "http://feeds.feedburner.com/TechCrunch/startups", "hashtags" : "#startups", "via" : "@techcrunch"},
        {"url" : "http://feeds.feedburner.com/TechCrunch/fundings-exits", "hashtags" : "#fundings", "via" : "@techcrunch"}
    ],
    "retweet" :
    {
        "max_retweets" : 600,
        "max_likes" : 600,
        "keywords" : [],
        "nbpages" : 40,
        "retweet_prob" : 0.5,
        "limit_prob" : 1.0
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
    "follow_unfollow_ratio_limit" : 1.2,
    "interval" : [30, 45]
}
```

* The max_new_followers set the maximum user that can be followed each day;
* The max_new_unfollow set the maximum user that can be unfollowed each day;
* The interval parameter set the interval in minutes between each follow/unfollow action choosen randomly between the min and the max;

### Create database

You have then to create the database on your MySQL host

    python pyTweetBot.py tools
        --create-database : Create the database structure on the MySQL host
        --export-database : Export tweets, tweeted and followers/friends to a file
        --import-database     Import tweets, tweeted and followers/friends from a file
        --file : File to import / to export to

You can use the "create-database" action for that :

    python pyTweetBot.py tools --config /path/to/config.json --create

It is possible to export bot's data to a file with the export-database command.

    python pyTweetBot.py tools --config /path/to/config.json --export --file export_file.p

And then import the bot's data from the file

    python pyTweetBot.py tools --config /path/to/config.json --import --file export_file.p

## Model training

### Create a dataset

### Train a model

## Command line

### Launch executors

pyTweetBot launch an executor thread for each action type. You can launch the executor daemon that way :

    python pyTweetBot.py executor --config /etc/bots/bot.conf

### Find new tweets

    python pyTweetBot.py find-tweets --config /etc/bots/bot.conf --model /etc/bots/models/find_tweets.p

### Find new retweets

    python pyTweetBot.py find-retweets --config /etc/bots/bot.conf --model /etc/bots/moedls/find_retweets.p

### Automatise execution with crontab

## Development

### Files

* [pyTweetBot.py](pyTweetBot.py) : Main Python file;
* [find_tweets.py](find_tweets.py) : Python code to find new contents to tweet;
