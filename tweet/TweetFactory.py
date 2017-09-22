#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
from patterns.singleton import singleton


@singleton
class TweetFactory(object):
    """
    Tweet Factory
    """

    # Constructor
    def __init__(self, hashtags=None, via=None):
        """
        Constructor
        :param hashtags:
        """
        self._hashtags = hashtags
        self._via = via
    # end __init__

    ##########################################
    # Public functions
    ##########################################

    # Create tweet text
    def __call__(self, text):
        """
        Create tweet text.
        :param text:
        :return:
        """
        # Clean
        cleaned_text = text.replace(u'\n', u'').replace(u'\r', u'')

        # Replace words by hashtags
        hashtags_text = self._replace_hashtags(cleaned_text)

        return hashtags_text
    # end __call__

    ##########################################
    # Private functions
    ##########################################

    # Replace a word by a hashtag
    def _word_to_hashtag(self, word, hashtag, prefix, suffix, text, case_sensitive=False):
        """
        Replace a word by a hashtag
        :param word:
        :param hashtag:
        :param text:
        :return:
        """
        if hashtag not in text:
            text = text.replace(prefix + word + suffix, prefix + hashtag + suffix)
            if not case_sensitive:
                text = text.replace(prefix + word.lower() + suffix, prefix + hashtag + suffix)
                text = text.replace(prefix + word.upper() + suffix, prefix + hashtag + suffix)
                text = text.replace(prefix + word.title() + suffix, prefix + hashtag + suffix)
            # end if
        # end if
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
            # Case sensitive
            case_sensitive = hashtag['case_sensitive'] if 'case_sensitive' in hashtag.keys() else False

            # Replace
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u' ', suffix=u'',
                                         text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u'', suffix=u' ',
                                         text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u'', suffix=u'\'s',
                                         text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u'', suffix=u':',
                                         text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u'', suffix=u',',
                                         text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'], hashtag=hashtag['to'], prefix=u'(', suffix=u')',
                                         text=text, case_sensitive=case_sensitive)

            # No space
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u' ',
                                         suffix=u'', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u' ', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u'\'s', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u':', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u',', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'(',
                                         suffix=u')', text=text, case_sensitive=case_sensitive)

            # No barre
            text = self._word_to_hashtag(word=hashtag['from'].replace(u'-', u''), hashtag=hashtag['to'], prefix=u' ',
                                         suffix=u'', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u'-', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u' ', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u'-', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u'\'s', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u'-', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u':', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u'-', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u',', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'(',
                                         suffix=u')', text=text, case_sensitive=case_sensitive)
        # end for
        return text.replace(u"##", u"#").replace(u"##", u"#").replace(u"##", u"#")
    # end replace_hashtags

# end TweetPreparator
