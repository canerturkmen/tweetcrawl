#!/usr/bin/python

from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection
from crawler.base import BaseCrawler

_crawler = BaseCrawler()
_crawler.run()
