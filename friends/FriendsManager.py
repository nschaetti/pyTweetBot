
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

    # Update
    def update(self):
        # Twitter connection
        twitter_con = TweetBotConnector()

        # Get followers
        """followers = twitter_con.get_followers(n_pages=1)

        # For each followers
        for follower in followers:
            print(follower.screen_name)
        # end for"""
        print(twitter_con.next())
    # end update

# end FriendsManager
