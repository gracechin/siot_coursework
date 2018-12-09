from twython import TwythonStreamer
from google_sheet import enter_twitter
import csv

# Enter your keys/secrets as strings in the following fields
credentials = {}
credentials['CONSUMER_KEY'] =
credentials['CONSUMER_SECRET'] =
credentials['ACCESS_TOKEN'] =
credentials['ACCESS_SECRET'] =

# Filter out unwanted data
def process_tweet(tweet):
    d = {}
    d['hashtags'] = ','.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]).encode('utf-8')
    d['text'] = tweet['text'].encode('utf-8')
    d['user'] = tweet['user']['screen_name'].encode('utf-8')
    d['created_at'] = tweet['created_at'].encode('utf-8')
    d['user_loc'] = tweet['user']['location']
    print(d['user_loc'])
    return d

# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            self.write_to_googlesheet(tweet_data)
            # self.save_to_csv(tweet_data)

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

    # Save each tweet to csv file
    def save_to_csv(self, tweet):
        with open(r'saved_tweets.csv', 'a') as file:
            writer = csv.writer(file)
            try:
                writer.writerow(tweet.values())
            except:
                pass

    def write_to_googlesheet(self, tweet):
        enter_twitter(tweet.values())

# Instantiate from our streaming class
stream = MyStreamer(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                    credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
# Start the streamon', location='') # you can add locatin here for the ones related
stream.statuses.filter(track='air polluti