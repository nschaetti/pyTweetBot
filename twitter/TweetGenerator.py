#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from patterns.singleton import singleton


@singleton
class TweetGenerator(object):

    # Constructor
    def __init__(self, config=None):
        if config is not None:
            self._hashtags = config.get_hashtags()
        # end if
    # end __init__

    # Create tweet text
    def __call__(self, text, url):
        # Not more than 140 characters
        reduced_text = text[:140]

        # Introduce hashtags
        hashtags_text = self._replace_hashtags(reduced_text)

        # No return
        hashtags_text = hashtags_text.replace(u'\n', '').replace(u'\r', '')

        return hashtags_text + u" " + url
    # end __call__

    # Replace hashtags
    def _replace_hashtags(self, text):
        """
        Replace hashtags
        :param text:
        :return:
        """
        for hashtag in self._hashtags:
            # Normal, Lower, Upper
            text.replace(hashtag['from'], hashtag['to'])
            text.replace(hashtag['from'].lower(), hashtag['to'])
            text.replace(hashtag['from'].upper(), hashtag['to'])

            # Without space
            text.replace(hashtag['from'].replace(u' ', u''), hashtag['to'])
            text.replace(hashtag['from'].lower().replace(u' ', u''), hashtag['to'])
            text.replace(hashtag['from'].upper().replace(u' ', u''), hashtag['to'])
        # end for
        return text
    # end replace_hashtags

# end TweetGenerator
