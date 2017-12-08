#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Default configuration
default_config = \
{
	"scheduler" :
	{
		"sleep": [6, 13]
	},
	"hashtags":
	[
	],
	"friends" :
	{
		"max_new_followers" : 40,
		"max_new_unfollow" : 40,
		"follow_unfollow_ratio_limit" : 1.2,
		"interval" : [30, 45],
		"ratio" : 0.8
	},
	"forbidden_words" :
	[
	],
	"direct_message" : "",
	"news_settings" : {
		"max_tweets" : 1200,
		"exclude" : [],
		"interval" : [2.0, 4.0]
	},
	"news" :
	[
	],
	"rss" :
	[
	],
	"retweet" :
	{
		"max_retweets" : 600,
		"max_likes" : 600,
		"keywords" : [],
		"nbpages" : 40,
		"retweet_prob" : 0.5,
        "limit_prob" : 1.0,
		"interval" : [2.0, 4.0]
	}
}
