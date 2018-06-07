#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : convert_dataset.py
# Description : Convert a dataset from old format to the new one.
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
# along with pyTweetBot.  If not, see <http://www.gnu.org/licenses/>.
#
"""This file contains a command line tool to convert a dataset from
the old format to the new one. The old format is composed of two lists
of URLs and texts. The new dataset format is a Dataset object containing
texts and class labels. This tool will download all the page's text
of the URls contained in the old dataset.

Example:
    Here is a simple example to convert a file::

        $ python convert_dataset.py --input old.p --output new.p
"""

# Import
import argparse
import os
import pickle
import sys
from learning.Dataset import Dataset
from tools.PageParser import PageParser, PageParserRetrievalError

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
            print(u"Retrieving URL {}/{} : {}".format(index+1, len(urls.keys()), url))

            # Get page's text
            try:
                page_text = PageParser.get_text(url)
            except PageParserRetrievalError as e:
                sys.stderr.write(u"Page retrieval error : {}".format(e))
                continue
            # end try

            # Not already in
            if not dataset.is_in(page_text):
                # Class
                if urls[url] == "tweet":
                    print(u"Adding \"{}\" (len {}) as positive".format(url, len(page_text)))
                    check_added = dataset.add_positive(page_text)
                else:
                    print(u"Adding \"{}\" (len {}) as negative".format(url, len(page_text)))
                    check_added = dataset.add_negative(page_text)
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
