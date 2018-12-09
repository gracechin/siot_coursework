# https://stackabuse.com/accessing-the-twitter-api-with-python/
import json
from twython import Twython
import pandas as pd

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] = "HPo1fKvKHLBjfNgQMzAvWMmnU"
credentials['CONSUMER_SECRET'] = "tXLfD3tGqf3QiGFhIu7GiPJ3w0gtZeaJdqNl815bxQVrcbD9y1"
credentials['ACCESS_TOKEN'] = "75251127-mx4Ywt3edUQmmzhG44MinpirrCSA4BecA2H8PXOXb"
credentials['ACCESS_SECRET'] = "dZGTs5oyCIU2Z2HEXX1sOwdQLlUjYqTfRO3jzgoYUKryU"

# # Load credentials from json file
# with open("twitter_credentials.json", "r") as file:
#     creds = json.load(file)

# Instantiate an object
python_tweets = Twython(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])

# Create our query
query = {'q': 'trump',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        }

# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])
    break

print dict_