from twython import TwythonStreamer
from google_sheet import enter_twitter
import csv
import json

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    credentials = json.load(file)

# Filter out unwanted data
def process_tweet(tweet):
    d = []
    d.append( tweet['created_at'].encode('utf-8')[:-10]) #created at
    d.append(tweet['text'].encode('utf-8')) # text
    d.append(tweet['user']['screen_name'].encode('utf-8')) # username
    d.append(','.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]).encode('utf-8')) # hashtags
    d.append(tweet['user']['location'])
    print(tweet['created_at'])
    return d

def add_location(data):
    location = []
    place_list = [["London", "England","UK"], ["Birmingham", "England","UK"], ["Manchester", "England","UK"], ["Leeds", "England","UK"],
                 ["Edinburgh", "Scotland","UK"], ["Glasgow", "Scotland","UK"], ["Swansea", "Wales","UK"], ["Plymouth", "England","UK"],
                 ["Los Angeles", "California", "USA"], ["Beaumont", "Texas", "USA"], ["Orlando","Florida","USA"], ["Chicago","Illinois","USA"], ["Atlanta","Georgia","USA"], ["United States"]
                 ["Hamamachi","Kyoto","Japan"], ["Chiyoda", "Tokyo","Japan"], ["Ao","Osaka", "Japan"],
                 ["Delhi","Delhi","India"], ["New Delhi","Delhi","India"],
                 ["Hong Kong","Hong Kong","Hong Kong"]]
    for full_loc in place_list:
        for loc in full_loc:
            user_loc = data[-1]
            if loc in user_loc:
                location.append(loc)
                if len(location)>1:
                    location = full_loc
        if len(location)>0:
            location = (",").join(location)
            break
    if len(location)==0:
        location = "other"
    return location


# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet_data = process_tweet(data)
            if tweet_data[-1] is not None:
                tweet_data.append(add_location(tweet_data))
            print(tweet_data)
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
                writer.writerow(tweet)
            except:
                pass

    def write_to_googlesheet(self, tweet):
        enter_twitter(tweet)

# Instantiate from our streaming class
stream = MyStreamer(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                    credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
# Start the streamon', location='') # you can add location here for the ones related
stream.statuses.filter(track='air pollution')