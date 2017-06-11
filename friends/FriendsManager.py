
from patterns.singleton import singleton
from db.DBConnector import DBConnector
from db.Friend import Friend
from twitter.TweetBotConnect import TweetBotConnector


@singleton
class FriendsManager(object):

    # Get followers
    @staticmethod
    def get_followers():
        """
        Get followers
        :return: Follower list
        """
        session = DBConnector().get_session()
        return session.query(Friend).all()
    # end get_followers

    # Follower exists
    def exists(self, follower):
        session = DBConnector().get_session()
        if type(follower) == "str":

        # end if
    # end exists

    # Update
    def update(self):
        # Twitter connection
        twitter_con = TweetBotConnector()

        # Get followers
        followers = twitter_con.get_followers(n_pages=1)

        # Get follower cursor
        cursor = twitter_con.get_followers_cursor()

        # For each page
        for page in cursor:
            # For each follower
            for follower in page:
                if not self._exists(follower):
                    self._add_follower(follower)
                else:
                    return
                # end if
            # end for
        # end for
    # end update

# end FriendsManager
