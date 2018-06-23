#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


class TweetPreparator(object):
    """
    Tweet preparator
    """

    # Constructor
    def __init__(self, hashtags=None):
        """
        Constructor
        :param hashtags:
        """
        self._hashtags = hashtags
    # end __init__

    ##########################################
    #
    # Public functions
    #
    ##########################################

    # Create tweet text
    def __call__(self, tweet):
        # Introduce hashtags
        hashtags_text = self._replace_hashtags(tweet.get_text())

        # No return
        hashtags_text = hashtags_text.replace(u'\n', '').replace(u'\r', '')

        # Not more than Tweet.MAX_LENGTH characters
        reduced_text = hashtags_text[:Tweet.MAX_LENGTH]

        # Change
        tweet.set_text(reduced_text)

        return tweet
    # end __call__

    ##########################################
    #
    # Private functions
    #
    ##########################################

    # Replace hashtags
    def _replace_hashtags(self, text):
        """
        Replace hashtags
        :param text:
        :return:
        """
        for hashtag in self._hashtags:
            # Normal, Lower, Upper
            text = text.replace(hashtag['from'], hashtag['to'])
            text = text.replace(hashtag['from'].lower(), hashtag['to'])
            text = text.replace(hashtag['from'].upper(), hashtag['to'])

            # Without space
            text = text.replace(hashtag['from'].replace(u' ', u''), hashtag['to'])
            text = text.replace(hashtag['from'].lower().replace(u' ', u''), hashtag['to'])
            text = text.replace(hashtag['from'].upper().replace(u' ', u''), hashtag['to'])
        # end for
        return text.replace(u"##", u"#").replace(u"##", u"#")
    # end replace_hashtags

# end TweetPreparator
