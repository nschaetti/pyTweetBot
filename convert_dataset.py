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
        with open(args.output, 'r') as f:
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

    # For each texts
    for url in urls.keys():
        print(u"Retrieving URL {}".format(url))
        # Get title
        soup = BeautifulSoup(urllib2.urlopen("https://www.google.com"))
        title = soup.title.string

        # Class
        if urls[url] == "tweet":
            print(u"Adding \"{}\" as positive".format(title))
            dataset.add_pos(title, url)
        else:
            print(u"Adding \"{}\" as negative".format(title))
            dataset.add_neg(title, url)
        # end if
    # end for

    # Save dataset
    dataset.save()

# end if
