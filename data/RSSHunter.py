
import feedparser


class RSSHunter(object):

    # Constructor
    def __init__(self, url):
        self._feed_url = url
    # end __init__

    # Parse
    def parse(self):
        print(feedparser.parse(self._feed_url))
    # end parse

# end RSSHunter
