#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


class TweetFactory(object):
    """
    Tweet Factory
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

        # Not more than 140 characters
        reduced_text = hashtags_text[:140]

        # Change
        tweet.set_text(reduced_text)

        return tweet
    # end __call__

    ##########################################
    #
    # Private functions
    #
    ##########################################

    # Replace a word by a hashtag
    def _word_to_hashtag(self, word, hashtag, text):
        """
        Replace a word by a hashtag
        :param word:
        :param hashtag:
        :param text:
        :return:
        """
        text = text.replace(word, hashtag)
        text = text.replace(word.lower(), hashtag)
        text = text.replace(word.upper(), hashtag)
        return text
    # end _word_to_hashtag

    # Replace hashtags
    def _replace_hashtags(self, text):
        """
        Replace hashtags
        :param text:
        :return:
        """
        for hashtag in self._hashtags:
            # Normal, Lower, Upper
            text = self._word_to_hashtag(word=hashtag['from'] + u' ', hashtag=hashtag['to'], text=text)
            text = self._word_to_hashtag(word=u' ' + hashtag['from'], hashtag=hashtag['to'], text=text)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u'') + u' ', hashtag=hashtag['to'], text=text)
            text = self._word_to_hashtag(word=u' ' + hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], text=text)
        # end for
        return text.replace(u"##", u"#").replace(u"##", u"#")
    # end replace_hashtags

# end TweetPreparator
