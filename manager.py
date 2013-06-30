#!/usr/bin/python

from twapi.api import TwCrawlAPI
from twitter import TwitterError

try:
    a = TwCrawlAPI()
    print a.getUserFollowers("canerturkmen")
#    print a.getRateLimitStatus()
except TwitterError as e:
#    print e.errno
    print e