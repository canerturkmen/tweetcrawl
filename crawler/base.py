from config import USER_FIELDS
from twapi.api import TwCrawlAPI
from twitter import TwitterError
from db.backend import DBConnection
import time, sys, logging, traceback


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
        currentId = 20505706
        self._logger.info("Initializing run for BaseCrawler")
        try:
            followers = self._api.getUserFollowers(currentId)
            for i in followers:
                self._db.persistUser({key: i[key] for key in USER_FIELDS})
                self._db.persistFollowLink(i['id'], currentId)
#                except:
#                    self._logger.warning("Error encountered. Possibly index related.")

        except TwitterError as e:
            self._logger.error("TwitterError encountered.")
            self._logger.error("Print StackTrace : \n %s" % traceback.format_exc())

        except:
            self._logger.critical("Error encountered.")
            sys.exit(status=0)


        self._logger.info("Sleeping for 1 minute")
        time.sleep(60) # sleep for 60 seconds
        self._logger.info("Slept for 1 minute")
