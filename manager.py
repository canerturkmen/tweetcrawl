#!/usr/bin/python

from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection

try:
    a = TwCrawlAPI()
    followers = a.getUserFollowers("canerturkmen")
    for i in followers:
        DBConnection.persistUser(i)
except TwitterError as e:
#    print e.errno
    print e[0][0]['code']