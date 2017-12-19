# pyTweetBot
A Twitter bot written in Python to replace yourself, search and publish news about specific subjects on Twitter.

## Installation

### Configuration file

pyTweetBot takes its configuration in a JSON file which looks as follow :

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

    "twitter" :
    {
        "auth_token1" : "",
        "auth_token2" : "",
        "access_token1" : "",
        "access_token2" : "",
        "user" : ""
    }

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

    python pyTweetBot.py database
        --create : Create the database structure on the MySQL host
        --export : Export tweets, tweeted and followers/friends to a file
        --file : File to import / to export to

You can use the "create" action for that :

    python pyTweetBot.py --config /path/to/config.json --create

It is possible to export bot's data to a file with the export command.

    python pyTweetBot.py --config /path/to/config.json --export --file export_file.p

And then import the bot's data from the file

    python pyTweetBot.py --config /path/to/config.json --import --file export_file.p

## Model training

### Create a dataset

### Train a model

## Find new tweets

    python pyTweetBot find-tweets --config /etc/bots/bot.conf --model /etc/bots/models/find_tweets.p

## Find new retweets

    python pyTweetBot find-retweets --config /etc/bots/bot.conf --model /etc/bots/moedls/find_retweets.p

## Automatise execution with crontab
