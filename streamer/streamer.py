"""
A Twitter Streaming API v1.1 client for retrieving tweets in a certain language
"""

import oauth2 as oauth
import httplib
import urllib
import time
import config
import simplejson as json
from orm.models import Tweet

class Streamer():
    """
    A streamer object encapsulates a client for the Twitter Streaming API
    """

    def __init__(self):
        self.consumer = oauth.Consumer(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
        self.token    = oauth.Token(config.TWITTER_ACCESS_TOKEN_KEY, config.TWITTER_ACCESS_TOKEN_SECRET)
        self.url      = "https://stream.twitter.com/1.1"

    def oauth_request(self, url, body):
        consumer = self.consumer
        token = self.token

        params = {
            "oauth_version"      : "1.0",
            "oauth_nonce"        : oauth.generate_nonce(),
            "oauth_timestamp"    : int(time.time()),
            "oauth_token"        : token.key,
            "oauth_consumer_key" : consumer.key,
            }
        params.update(body)

        request = oauth.Request("POST", url, params)
        request.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)
        return request

    def _get_buffer(self):
        buffer = ""

        while True:
            try:
                readval = self.response.read(1)
            except httplib.HTTPException:
                continue
            except:
                print "unknown error encountered"

            if readval == "\n":
                break
            else:
                buffer += readval

        buffer = buffer.strip()
        if buffer and buffer.isdigit():
            return int(buffer)

    def main(self, **kwargs):
        kwargs['delimited'] = 'length'

        url = self.url + "/statuses/filter.json"
        data = self.oauth_request(url, kwargs)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        connection = httplib.HTTPSConnection("stream.twitter.com")
        connection.set_debuglevel(1)

        connection.request(
            method = "POST",
            url = "/1.1/statuses/filter.json",
            body = urllib.urlencode(data),
            headers = headers)

        self.response = connection.getresponse()

        while True:
            length = self._get_buffer()
            if length:
                update = self.response.read(length)
                update = json.loads(update)
                tw = Tweet(fulldata=update)
                tw.save()
                print update


            else:
                print "ping!"

