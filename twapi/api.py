from .request import twRequest
import config, twitter


class TwCrawlAPI:
    """
    Twitter API wrapper for the following functions:
    GET users/lookup
    GET users/show

    """
    _api = None

    def __init__(self):
        self._api = twitter.Api(config.TWITTER_CONSUMER_KEY,
                                config.TWITTER_CONSUMER_SECRET,
                                config.TWITTER_ACCESS_TOKEN_KEY,
                                config.TWITTER_ACCESS_TOKEN_SECRET)


    def getUserProfile(self,user):
        if type(user) is str:
            result=self._api.GetUser(screen_name=user)
        elif type(user) is int:
            result=self._api.GetUser(user_id=user)

        return str(result)

    def getUserFollowers(self, user):
        if type(user) is str:
            result = self._api.GetFollowers(screen_name=user)
        elif type(user) is int:
            result = self._api.GetFollowers(user_id=user)

        return result

    def getRateLimitStatus(self):
        return self._api.GetRateLimitStatus()

