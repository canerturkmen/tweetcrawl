from config import USER_FIELDS
from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection
import time, sys, logging, traceback
import threading


class BaseCrawler:

    def __init__(self):
        logging.basicConfig(#filename="logs/twcrawl_log_%s.log" % datetime.now().strftime("%Y%m%d_%H%M"),
                            filename="logs/twcrawl_log_.log",
                            format='%(asctime)-15s %(levelname)s : %(message)s',
                            level=logging.INFO)
        self._logger = logging.getLogger()
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
        currentId = 20505706
        self._logger.info("Initializing run for BaseCrawler")
        try:
            followers = self._api.getUserFollowers(currentId)
#             print self._api.getRateLimitStatus()
            for user_object in followers:
                user_dict = user_object.AsDict()
                self._db.persistUser({key: user_dict[key] for key in USER_FIELDS})
#                self._db.persistFollowLink(i['id'], currentId)
#                except:
#                    self._logger.warning("Error encountered. Possibly index related.")

        except TwitterError as e:
            self._logger.error("TwitterError encountered.")
            self._logger.error("Print StackTrace : \n %s" % traceback.format_exc())

#        except:
#            self._logger.critical("Error encountered.")
#            sys.exit()


        self._logger.info("Sleeping for 1 minute")
        time.sleep(60) # sleep for 60 seconds
        self._logger.info("Slept for 1 minute")

        self._logger.info("Exiting main thread")

    def logDaemon(self):
        """
        A simple daemon thread that regularly updates the status of the app and the database
        on the log
        """
        self._logger.info("Log daemon is up and running")
        while(True):
            self._logger.info("App is running")
            self._logger.info("Tweets count is: %s" % str(self._db.getTablesCounts()))
            time.sleep(10)