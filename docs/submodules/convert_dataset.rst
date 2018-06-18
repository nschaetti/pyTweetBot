pyTweetBot.convert_dataset
==========================

This file contains a command line tool to convert a dataset from
the old format to the new one. The old format is composed of two lists
of URLs and texts. The new dataset format is a Dataset object containing
texts and class labels. This tool will download all the page's text
of the URls contained in the old dataset.

Example:
    Here is a simple example to convert a file::

        $ python convert_dataset.py --input old.p --output new.p
