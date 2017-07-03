#!/usr/bin/env python
# -*- coding: utf-8 -*-
#


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
    #
    # Public functions
    #
    ##########################################

    # Create tweet text
    def __call__(self, tweet):
        """
        Create tweet text.
        :param tweet:
        :return:
        """
        # Clean
        cleaned_text = tweet.get_text().replace(u'\n', '').replace(u'\r', '')

        # Check tweet length
        #if not self._check_text_length(cleaned_text):
        #    cleaned_text = self._reduce_tweet(cleaned_text)
        # end if

        # Replace words by hashtags
        hashtags_text = self._replace_hashtags(cleaned_text)

        # Add via if possible
        #if self._via is not None and self._check_text_length(hashtags_text + u" via " + self._via):
        #    via_text = self._add_via(hashtags_text, self._via)
        #else
        #    via_text = hashtags_text
        # end if

        # Change
        tweet.set_text(hashtags_text)

        return tweet
    # end __call__

    ##########################################
    #
    # Private functions
    #
    ##########################################

    # Add via
    def _add_via(self, text, via):
        """
        Add via information
        :param text:
        :param via:
        :return:
        """
        return text + u" via " + via
    # end _add_via

    # Reduce text
    def _reduce_tweet(self, text, url_present):
        """
        Reduce text
        :param tweet:
        :return:
        """
        if url_present:
            return text[:140-24-3] + u"..."
        else:
            return text[:140-3] + u"..."
        # end if
    # end if

    # Check Tweet length
    def _check_length(self, tweet):
        """
        Check Tweet length
        :param text:
        :return:
        """
        if tweet.get_url() != "":
            return len(tweet.get_text()) + 24 <= 140
        else:
            return len(tweet.get_text()) <= 140
        # end if
    # end _check_length

    # Check Tweet length
    def _check_text_length(self, text, url_present):
        """
        Check Tweet length
        :param text:
        :return:
        """
        if url_present:
            return len(text) + 24 <= 140
        else:
            return len(text) <= 140
        # end if
    # end _check_length

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
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u' ',
                                         suffix=u'', text=text, case_sensitive=case_sensitive)
            text = self._word_to_hashtag(word=hashtag['from'].replace(u' ', u''), hashtag=hashtag['to'], prefix=u'',
                                         suffix=u' ', text=text, case_sensitive=case_sensitive)
        # end for
        return text.replace(u"##", u"#").replace(u"##", u"#")
    # end replace_hashtags

# end TweetPreparator
