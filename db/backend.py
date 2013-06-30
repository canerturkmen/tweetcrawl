from pymongo import MongoClient, collection
from config import MONGODB_HOST, MONGODB_PORT
import twitter

class DBConnection:
    """
    Class for encapsulating the DB connection context for tweetcrawl application.
    Loosely follows the Singleton pattern, although the pattern could be enhanced using python __metaclass__
    """

    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(MONGODB_HOST, MONGODB_PORT)
            except:
                cls._instance = MongoClient()

        return cls._instance

    @classmethod
    def persistUser(cls, user):
        """
        Persists a python-twitter User object in the MongoDB database
        :type user: twitter.User
        """
        if type(user) is twitter.User:
            table = cls.getInstance().twcrawl.users
            return table.insert(user.AsDict())
        else:
            return False

    @classmethod
    def persistStatus(cls, status):
        """
        Persists a python-twitter Status object in the MongoDB database

        Params:
        :type status: twitter.Status
        status: the twitter.Status object to be saved in the database

        Returns:
        false, or the mongodb document reference if persist successful
        """
        if type(status) is twitter.Status:
            table = cls.getInstance().twcrawl.tweets
            return table.insert(status.AsDict())
        else:
            return False

