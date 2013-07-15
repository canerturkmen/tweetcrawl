"""
Base ActiveRecord-like model for our simple ORM
"""
import logging
import traceback
from pymongo.errors import DuplicateKeyError
from config import DB_NAME
from db.backend import DBConnection

class BaseRecord():
    """
    BaseRecord encapsulates the mongodb-persistable ORM base object type in tweetcrawl.
    """
    _dbhandle = DBConnection.getInstance()[DB_NAME]
    _logger = logging.getLogger(__name__)

    def __init__(self):
        """
        Under normal circumstances, the base constructor should not be called (class should not be instantiated).
        This is why this method call raises NotImplementedError

        :raises: NotImplementedError
        """
        raise NotImplementedError("I'm an abstract class, you cannot instantiate me")

    def initialize(self, kwargs):
        """
        This method initializes the ORM record, called by the constructor method of inheriting classes.

        The method sets the MongoDB collection name to the class name's lowercase version, and instantiates
        an empty ``dict``.

        :raises: AttributeError
        """
        self._collection = self._dbhandle[self.__class__.__name__.lower()]
        self._data = {}
        if kwargs.keys().__len__() == 0:
            raise AttributeError("You must pass me at least one argument to initialize a tweet")

        if kwargs.has_key("fulldata"):
            tw = kwargs.get("fulldata")
            for field in self._schema.get("fields"):
                if field == "id":
                    self._data["_id"] = tw.get(field)
                else:
                    self._data[field] = tw.get(field)
        else:
            for field in self._schema.get("fields"):
                if field == "id":
                    self._data["_id"] = kwargs.get(field)
                else:
                    self._data[field] = kwargs.get(field)

    def save(self, **kwargs):
        try:
            self._collection.insert(self._data)
        except DuplicateKeyError:
            self._logger.warning("pymongo raised DuplicateKeyError")
        except:
            self._logger.error("Exception raised while trying to insert record")
            self._logger.error("Printing StackTrace : \n %s" % traceback.format_exc())

    @classmethod
    def getAll(cls):
        cls._collection = cls._dbhandle[cls.__name__.lower()]
        return cls._collection.find()
