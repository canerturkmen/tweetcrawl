"""
Base ActiveRecord-like model for our simple ORM
"""
import logging
from config import DB_NAME
from db.backend import DBConnection

class BaseRecord():

    _dbhandle = DBConnection.getInstance()[DB_NAME]
    _logger = logging.getLogger(__name__)

    def __init__(self):
        raise NotImplementedError("I'm an abstract class, you cannot instantiate me")

    def initialize(self, kwargs):
        self._collection = self._dbhandle[self.__class__.__name__.lower()]
        self._data = {}
        if kwargs.keys().__len__() == 0:
            raise AttributeError("You must pass me at least one argument to initialize a tweet")

        if kwargs.has_key("fulldata"):
            tw = kwargs.get("fulldata")
            for field in self._schema.get("fields"):
                self._data[field] = tw[field]
        else:
            for field in self._schema.get("fields"):
                self._data[field] = kwargs.get(field)

    def save(self, **kwargs):
        try:
            self._collection.insert(self._data)
        except:
            self._logger.error("Exception raised while trying to insert record")

    @classmethod
    def getAll(cls):
        cls._collection = cls._dbhandle[cls.__name__.lower()]
        return cls._collection.find()
