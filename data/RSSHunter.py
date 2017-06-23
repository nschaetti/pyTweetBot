
import feedparser


class RSSHunter(object):

    # Constructor
    def __init__(self, url):
        self._feed_url = url
        self._counter = 0
    # end __init__

    # Parse
    def parse(self):
        for entry in feedparser.parse(self._feed_url)['entries']:
            print(entry['title'])
            print("")
        # end for
    # end parse

    def __iter__(self):
        self._counter = 0
    # end __iter__

# end RSSHunter
