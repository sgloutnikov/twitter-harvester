import twitter
import os
import json

# Twitter API Credentials
consumer_key = 'DCe7buvPLhAXoBEEptW5w'
access_token = '1025063461-f3m1fLtohYx5a7HILOgFu5R23eY1yvPJCT9cwTm'
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')


api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret)

tracked_hashtags = [
    "#nba"
]

stream = api.GetStreamFilter(track=tracked_hashtags)

for line in stream:
    print(json.dumps(line))

