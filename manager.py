
from twapi.api import TwCrawlAPI

try:
    a = TwCrawlAPI()
    print a.getUserFollowers("canerturkmen")
except BaseException:
    pass