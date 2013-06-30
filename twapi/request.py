from urllib2 import Request, urlopen
from urllib import urlencode
from config import *
import json

def twRequest(api_url, params=None):
    request_url = TWITTER_API_URL + api_url
    if params:
        request_url += "?" + urlencode(params)
    response = urlopen(request_url)
    hypertext = response.read()

    return json.loads(hypertext)
