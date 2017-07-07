import twitter
import os
from pymongo import MongoClient
import logging.config


# Twitter API Credentials
consumer_key = 'DCe7buvPLhAXoBEEptW5w'
access_token = '1025063461-f3m1fLtohYx5a7HILOgFu5R23eY1yvPJCT9cwTm'
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

# Logging
log_config = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Tracked Hashtags
tracked_hashtags = [
    "#agt"
]

logger.info("Starting up...")


def remove_key(json, key):
    try:
        json.pop(key)
    except KeyError:
        pass


MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)


stream = api.GetStreamFilter(track=tracked_hashtags)

for tweet in stream:
    tweet['_id'] = tweet.pop('id_str')
    # Cleanup
    remove_key(tweet, 'id')
    remove_key(tweet, 'display_text_range')
    remove_key(tweet, 'in_reply_to_status_id')
    remove_key(tweet, 'in_reply_to_user_id')
    remove_key(tweet, 'quoted_status_id')
    remove_key(tweet, 'quoted_status')
    remove_key(tweet, 'entities')
    remove_key(tweet, 'extended_entities')
    remove_key(tweet, 'current_user_retweet')
    try:
        if tweet['retweeted_status']:
            tweet['retweeted_status_id_str'] = tweet['retweeted_status']['id_str']
            remove_key(tweet, 'retweeted_status')
    except KeyError:
        pass
    # User
    user = tweet.pop('user')
    user['_id'] = user.pop('id_str')
    tweet['user_id'] = user['_id']
    user.pop('id')
    # Place
    if tweet['place']:
        # TODO: Check if id is unique per place and if data will be lost if replace is used
        place = tweet.pop('place')
        tweet['place_id'] = place['id']
        db.places.insert_one(place)
    # DB Inserts
    db.users.replace_one({'_id': user['_id']}, user, upsert=True)
    result = db.tweets.insert_one(tweet)
    logger.info(result)
