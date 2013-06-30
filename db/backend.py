from pymongo import MongoClient
from config import MONGODB_HOST, MONGODB_PORT
import twitter

class DBConnection:
    """
    Class for encapsulating the DB connection context for tweetcrawl application.
    Loosely follows the Singleton pattern, although the pattern could be enhanced using python __metaclass__
    """

    _instance = None

    @staticmethod
    def getInstance(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(MONGODB_HOST, MONGODB_PORT)
            except:
                cls._instance = MongoClient()

        return cls._instance

    def persistUser(cls, user):
        if type(user) is twitter.User:
            table = cls.getInstance().users
            return table.insert(user.AsDict())
        else:
            return False

    def persistStatus(cls, status):
        """
        Persists a python-twitter Status object in the
        """
        if type(status) is twitter.Status:
            table = cls.getInstance().tweets
            return table.insert(tweet.AsDict())
        else:
            return False


