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
        if type(user) is dict:
            table = cls.getInstance().twcrawl.users
            return table.insert(user)
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

    @classmethod
    def persistFollowLink(cls, follower, friend):
        """
        Persists a 'follow-link', a directed arc of the social graph in Twitter, originating from the
        follower to the followed.

        Params:
        follower -- int, the twitter user id of the follower
        friend -- int, twitter user id of the user who is followed

        Returns:
        nothing
        """

        if type(follower) is not int or type(friend) is not int:
            raise TypeError
        table = cls.getInstance().twcrawl.followlinks
        try:
            hash = {'follower': follower, 'friend': friend}
            table.insert(hash)
        except:
            pass #TODO: Revise!

    @classmethod
    def getTablesCounts(cls):
        db = cls.getInstance().twcrawl
        result = {}
        for coll in db.collection_names():
            result[coll] = db[coll].count()
        return result
