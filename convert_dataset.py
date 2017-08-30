#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
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

# Import
import argparse
import os
import pickle
import urllib2
import sys
import socket
from BeautifulSoup import BeautifulSoup
from learning.Dataset import Dataset


####################################################
# Main function
####################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description=u"pyTweetBot - Convert to new dataset format")

    # Argument
    parser.add_argument("--input", type=str, help=u"Input dataset file", required=True)
    parser.add_argument("--output", type=str, help=u"Output dataset file", required=True)
    args = parser.parse_args()

    # Load old dataset
    if os.path.exists(args.input):
        with open(args.input, 'r') as f:
            (urls, texts) = pickle.load(f)
        # end with
    else:
        sys.stderr.write(u"Can't find dataset file {}\n".format(args.input))
        exit()
    # end if

    # Load new dataset
    if os.path.exists(args.output):
        dataset = Dataset.load(args.output)
    else:
        dataset = Dataset()
    # end if

    try:
        # For each texts
        index = 0
        for url in urls.keys():
            if not dataset.is_url_in(url):
                print(u"Retrieving URL {}".format(url))
                # Get title
                try:
                    soup = BeautifulSoup(urllib2.urlopen(url))
                except urllib2.HTTPError as e:
                    sys.stderr.write(u"HTTP error while retrieving {} : {}\n".format(url, e))
                    continue
                except socket.error as e:
                    sys.stderr.write(u"Socket error while retrieving {} : {}\n".format(url, e))
                    continue
                except urllib2.URLError as e:
                    sys.stderr.write(u"URL error while retrieving {} : {}\n".format(url, e))
                    continue
                # end try
                title = soup.title.string

                # Class
                if urls[url] == "tweet":
                    print(u"Adding \"{}\" as positive".format(title))
                    check_added = dataset.add_pos(title, url)
                else:
                    print(u"Adding \"{}\" as negative".format(title))
                    check_added = dataset.add_neg(title, url)
                # end if

                # Error handle
                if not check_added:
                    sys.stderr.write(u"URL {} is already in the dataset\n".format(url))
                # end if

                # Save dataset
                if index % 50 == 0:
                    print(u"Saving dataset to {}".format(args.output))
                    dataset.save(args.output)
                # end if

                index += 1
            # end if
        # end for
    except (KeyboardInterrupt, SystemExit):
        print(u"Saving dataset to {}".format(args.output))
        dataset.save(args.output)
    # end try
# end if
