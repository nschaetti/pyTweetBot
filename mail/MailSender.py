#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : mail/MailSender.py
# Description : pyTweetBot mail sender tool.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 15.08.2017 10:11
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

# Imports
import smtplib
import sys
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dns.resolver
import pyTweetBot.tools.strings as pystr


# Mail sender tool
class MailSender(object):
    """
    Mail sender tool
    """

    _subject = ""
    _from_address = ""
    _to_addresses = list()
    _msg = u""

    # Constructor
    def __init__(self, subject="", from_address="", to_addresses="", msg=""):
        """
        Constructor
        """
        # Properties
        self._subject = subject
        self._from_address = from_address
        self._to_addresses = to_addresses
        self._msg = msg
    # end __init__

    # Set subject
    def subject(self, subject):
        """
        Set subject
        :param subject:
        """
        self._subject = subject
    # end subject

    # Set from address
    def from_address(self, from_address):
        """
        Set source address
        :param from_address:
        :return:
        """
        self._from_address = from_address
    # end from_address

    # Set destination addresses
    def to_addresses(self, to_addresses):
        """
        Set destination addresses
        :param to_addresses:
        :return:
        """
        self._to_addresses = to_addresses
    # end to_addresses

    # Send mail
    def send(self):
        """
        Send mail
        :return: True if ok, False otherwise
        """
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self._subject
        msg['From'] = self._from_address
        msg['To'] = self._to_addresses[0]

        # Create the body of the message (a plain-text and an HTML version).
        text = self._msg
        html = self._msg

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        """answers = dns.resolver.query('gmail.com', 'MX')
        if len(answers) <= 0:
            logging.getLogger(pystr.LOGGER).error('No mail servers found for destination\n')
            return False
        # end if

        # Just pick the first answer
        print(answers[0].exchange)
        server = str(answers[0].exchange)

        # Send the message via local SMTP server.
        s = smtplib.SMTP(server)"""
        s = smtplib.SMTP("smtp.gmail.com:587")

        # EHLO & starttls
        s.ehlo()
        s.starttls()

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        try:
            print(self._to_addresses[0])
            print(msg.as_string())
            s.sendmail("pytweetbot@bot.ai", self._to_addresses[0], msg.as_string())
            s.quit()
        except smtplib.SMTPServerDisconnected as e:
            logging.getLogger(pystr.LOGGER).error(u"SMTP server disconnected : {}".format(e))
        # end try

        # Ok
        return True
    # end send

# end MailSender
