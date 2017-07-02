import twitter
import os
from pymongo import MongoClient, DESCENDING, ASCENDING


print("Starting harvester...")
# Twitter API Credentials
consumer_key = 'DCe7buvPLhAXoBEEptW5w'
access_token = '1025063461-f3m1fLtohYx5a7HILOgFu5R23eY1yvPJCT9cwTm'
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)

tracked_hashtags = [
    "#agt"
]

print("Beginning to listen to Streaming API")

stream = api.GetStreamFilter(track=tracked_hashtags)

for line in stream:
    result = db.twitter_dump.insert_one(line)
    print(result)

