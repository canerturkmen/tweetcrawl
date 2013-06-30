#!/usr/bin/python

from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection
from crawler.base import BaseCrawler

try:
    _crawler = BaseCrawler()
    _crawler.run()

except TwitterError as e:
#    print e.errno
    print e[0][0]['code']