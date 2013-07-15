from orm.base import BaseRecord


class Tweet(BaseRecord):
    """
    "created_at": <Date Time>,
    "id" : <18 digit or more integer>
    "id_str": "347997859016216576",
    "text":  <140 chars>,
    "user" : <User Record>,
    "geo": null,
    "coordinates": null,
    "place": null,
    <Retweeted status> : Data of the original tweet that user has retweeted, including use ??
    "retweet_count": 0,
    "favorite_count": 0,
    "entities": { "hashtags": [{ "text": "saitmaden", "indices": [ 121, 131 ] }],
        "symbols": [],
        4
        "urls": [],
        "user_mentions": []},
    "favorited": false,
    "retweeted": false,
    "lang": "tr"
    """

    _schema = {"fields": ["created_at", "id", "id_str", "text", "user", "geo", "coordinates", "place",
                          "retweeted","retweet_count" "favorite_count", "entities", "favorited", "retweeted", "lang"]}

    def __init__(self, **kwargs):
        self.initialize(kwargs)


class User(BaseRecord):
    """
    {
        "id": 461494325,
        "id_str": "461494325",
        "name": "Ali Taylan Cemgil",
        "screen_name": "AliTaylanCemgil",
        "location": "Istanbul",
        "protected": false,
        "followers_count": 155,
        "friends_count": 68,
        "created_at": "Wed Jan 11 21:29:16 +0000 2012",
        "profile_image_url": "http:\/\/a0.twimg.com\/profile_images\/3580500548\/0e33ddc524605cb
    }
    """

    _schema = {"fields": ["id", "id_str", "name", "screen_name", "location", "protected", "followers_count",
                          "friends_count", "created_at", "profile_image_url"]}

    def __init__(self, **kwargs):
        self.initialize(kwargs)

class FollowLink(BaseRecord):
    """
    Data model for encapsulating the follow link for a Twitter follow relationship
    """

    _schema = {"fields": ["follower_id", "friend_id", "follower_id_str", "friend_id_str", "created_at"]}

    def __init__(self, **kwargs):
        self.initialize(kwargs)
