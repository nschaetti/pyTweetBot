#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# Imports
import itertools
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

        # Add hashtags
        hashtags_text = self._add_hashtags(cleaned_text)

        return hashtags_text
    # end __call__

    ##########################################
    # Private functions
    ##########################################

    # Get possible capitalize words
    def _capitalized_set(self, text):
        """
        Get possible capitalized words
        :param text:
        :return:
        """
        # Separate by space
        words = text.split(u' ')

        # Combination
        return list(set(map(' '.join, itertools.product(*((w, w.upper(), w.lower(), w.title()) for w in words)))))
    # end _capitalized_set

    # Replace a word by a hashtag
    def _word_to_hashtag(self, word, hashtag, prefix, suffix, text, case_sensitive=False):
        """
        Replace a word by a hashtag
        :param word:
        :param hashtag:
        :param text:
        :return:
        """
        # Beginning
        if text[:len(word)] == word:
            text = hashtag + text[len(word):]
        # end if

        # Case sensitive
        if not case_sensitive:
            # Capitalized words
            upper_lower_combi = self._capitalized_set(word)
            for upper_lower_inst in upper_lower_combi:
                # Beginning
                if text[:len(word)] == upper_lower_inst or text[:len(word)] == upper_lower_inst.replace(u' ', u'') or text[:len(word)] == upper_lower_inst.replace(u'-', u''):
                    text = hashtag + text[len(word):]
                # end if
            # end for
        # end if

        # Inside
        if hashtag not in text:
            if len(prefix) > 0 or len(suffix) > 0:
                text = text.replace(prefix + word + suffix, prefix + hashtag + suffix)
                if not case_sensitive:
                    # Capitalized words
                    upper_lower_combi = self._capitalized_set(word)
                    for upper_lower_inst in upper_lower_combi:
                        text = text.replace(prefix + upper_lower_inst + suffix, prefix + hashtag + suffix)
                        text = text.replace(prefix + upper_lower_inst.replace(u' ', u'') + suffix, prefix + hashtag + suffix)
                        text = text.replace(prefix + upper_lower_inst.replace(u'-', u'') + suffix, prefix + hashtag + suffix)
                    # end for
                # end if
            # end if
        # end if

        # Outside
        if text[-len(word):] == word:
            text = text[:-len(word)] + hashtag
        # end if

        # Case sensitive
        if not case_sensitive:
            # Capitalized words
            upper_lower_combi = self._capitalized_set(word)
            for upper_lower_inst in upper_lower_combi:
                # Beginning
                if text[-len(word):] == upper_lower_inst or text[-len(word):] == upper_lower_inst.replace(u' ', u'') or text[-len(word):] == upper_lower_inst.replace(u'-', u''):
                    text = text[:-len(word)] + hashtag
                # end if
            # end for
        # end if

        return text
    # end _word_to_hashtag

    # Replace hashtag
    def _replace_hashtag(self, text, word, hashtag, prefix_suffix, case_sensitive):
        """
        Replace hashtag
        :param text:
        :param prefix_suffix:
        :return:
        """
        # Replace with each combinaison of suffix
        for prefix in prefix_suffix:
            for suffix in prefix_suffix:
                text = self._word_to_hashtag(word=word, hashtag=hashtag, prefix=prefix, suffix=suffix, text=text,
                                             case_sensitive=case_sensitive)
            # end for
        # end for

        # Return with no # doublon
        return text.replace(u"##", u"#").replace(u"##", u"#").replace(u"##", u"#")
    # end _replace_hashtag

    # Replace hashtags
    def _replace_hashtags(self, text):
        """
        Replace hashtags
        :param text:
        :return:
        """
        # For each hashtag
        for hashtag in self._hashtags:
            # Case sensitive
            case_sensitive = hashtag['case_sensitive'] if 'case_sensitive' in hashtag.keys() else False

            # Replace hashtags
            text = self._replace_hashtag(text=text, word=hashtag['from'], hashtag=hashtag['to'],
                                  prefix_suffix=[u' ', u'\'', u'(', u')', u':', u',', u'?', u'!', u'.', u'`', u';', u'\t', u'/', u'’'],
                                  case_sensitive=case_sensitive)
        # end for
        return text.replace(u"##", u"#").replace(u"##", u"#").replace(u"##", u"#")
    # end replace_hashtags

    # Add hashtags
    def _add_hashtags(self, text):
        """
        Add hashtags
        :param text:
        :return:
        """
        # For each hashtag
        for hashtag in self._hashtags:
            if len(u"{} #{}".format(tweet_text, topic)) + 21 < 140:
                tweet_text = u"{} #{}".format(tweet_text, topic)
            else:
                break
            # end if
        # end for

# end TweetPreparator
