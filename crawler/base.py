from db.backend import DBConnection
import logging
from datetime import datetime
from twapi.api import TwCrawlAPI
import time

class BaseCrawler:

    _logger = None

    def __init__(self):
        logging.basicConfig(filename="logs/twcrawl_log_%s.log" % datetime.now().strftime("%Y%m%d_%H%M"),
                            format='%(asctime)-15s %(message)s',
                            level=logging.INFO)
        self._logger = logging.getLogger()
#        self._db = DBConnection
        self._api = TwCrawlAPI()

    def run(self):
        self._logger.info("Initializing run for BaseCrawler")

        followers = self._api.getUserFollowers("canerturkmen")
        for i in followers:
            # DBConnection.persistUser(i)
            print i.AsDict
            break

        self._logger.info("Sleeping for 1 minute")
        time.sleep(60) # sleep for 60 seconds
        self._logger.info("Slept for 1 minute")
