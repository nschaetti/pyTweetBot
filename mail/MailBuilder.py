#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : mail/MailBuilder.py
# Description : pyTweetBot mail builder tool.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#


# Mail builder tool
class MailBuilder(object):
    """
    Mail builder tool
    """

    # Constructor
    def __init__(self, message_model):
        """
        Constructor
        """
        self._parameters = dict()
        self._message = message_model
    # end __init__

    # Get message
    def message(self):
        """
        Get message
        :return: Message as HTML code
        """
        message = self._message

        # Replace
        for key in self._parameters.keys():
            message = message.replace(u"@@_" + key + u"_@@", unicode(self._parameters[key]))
        # end for

        return message
    # end message

    # Set parameter
    def __setitem__(self, key, value):
        """
        Set parameter
        :param key:
        :param value:
        :return:
        """
        self._parameters[key] = value
    # end __setattr__

# end MailBuilder
