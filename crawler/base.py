from config import USER_FIELDS
from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection
import time, sys, logging, traceback
import threading


class BaseCrawler:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._db = DBConnection
        self._api = TwCrawlAPI()

    def run(self):
        """
        Implements two threads that will run (1) the crawler itself, (2) an auxiliary thread that will
        regularly update the user on the status of the database collections / app etc
        """
        threads = []
        threads.append(threading.Thread(target=self.crawl))

        threads.append(threading.Thread(target=self.logDaemon))
        threads[1].daemon = True

        for t in threads:
            t.start()

    def crawl(self):
        crawl_counter = 0
        while(True):
            currentId = 20505706
            crawl_counter += 1
            self._logger.info("Base crawler iteration initializing: iter no %s" % crawl_counter)

            try:
                followers = self._api.getUserFollowers(currentId)
                print self._api.getRateLimitStatus()
                for user_object in followers:
                    user_dict = user_object.AsDict()
                    user_dict = {key: user_dict.get(key) for key in USER_FIELDS}
                    user_dict['timeline_crawled'] = False
                    self._db.persistUser(user_dict)
                    self._db.persistFollowLink(user_dict['id'], currentId)

            except TwitterError as e:
                if e[0][0]['code'] == 88:
                    self._logger.warning("Base Crawler main thread encountered Rate Limit error")
                else:
                    self._logger.error("Base Crawler main thread: Unexpected TwitterError encountered.")
                    self._logger.error("Printing StackTrace : \n %s" % traceback.format_exc())

            except:
                self._logger.error("Base Crawler main thread encountered unexpected error.")
                self._logger.error("Printing StackTrace : \n %s" % traceback.format_exc())

            self._logger.info("Sleeping for 5 minutes")
            time.sleep(300) # sleep for 60 seconds
            self._logger.info("Slept for 5 minutes")

        self._logger.info("Exiting main thread")

    def logDaemon(self):
        """
        A simple daemon thread that regularly updates the status of the app and the database
        on the log
        """
        self._logger.info("Log daemon is up and running")
        while(True):
            self._logger.info("Database count is: %s" % str(self._db.getTablesCounts()))
            time.sleep(10)