#!/usr/bin/python

"""
Module that syncs the mongodb instance to desired schema for the application
A high level DB migration module
"""

from pymongo import *
from config import MONGODB_HOST, MONGODB_PORT, MONGO_ASCENDING, MONGO_DESCENDING

client = MongoClient(MONGODB_HOST, MONGODB_PORT)

# create database if not exists
db = client['twcrawl']

# create the collections required
db['tweets']
db['users']
db['followlinks']
db['hashtags']

# create ensureIndex constraints

db.tweets.ensure_index({"status_id": 1}, {"unique": True})
db.users.ensure_index({"user_id": 1}, {"unique": True})