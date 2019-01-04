from twython import TwythonStreamer
from google_sheet import enter_twitter
import csv
import json
import logging
from datetime import datetime

logging.basicConfig(filename='twitter_crawler.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    credentials = json.load(file)

# Filter out unwanted data
def process_tweet(tweet):
    d = []
    d.append(tweet['created_at'].encode('utf-8')[:-10])# created at
    d.append(tweet['created_at'].encode('utf-8')[:-20])# date
    d.append(tweet['created_at'].encode('utf-8')[-19:-10])# time
    d.append(tweet['text'].encode('utf-8')) # text
    d.append(tweet['user']['screen_name'].encode('utf-8')) # username
    d.append(','.join([hashtag['text'] for hashtag in tweet['entities']['hashtags']]).encode('utf-8')) # hashtags

    # adding location
    d.append(tweet['user']['location'])
    if tweet['user']['location']:
        spec_location = specify_location(tweet['user']['location'])
        d.append(spec_location[1])
        d.append(spec_location[0])
    else:
        d.append('n/a')
        d.append('-')
    return d

def file_to_lists(filename):
    file = open(filename, "r")
    lines = file.read().splitlines()
    return lines

def specify_location(user_loc):
    output = []
    location = []
    UK_list = file_to_lists("UK_list.txt")
    US_list = file_to_lists("US_list.txt")
    IN_list = file_to_lists("IN_list.txt")
    HK_list = file_to_lists("HK_list.txt")
    UK_dict = {"UK":UK_list}
    US_dict = {"US":US_list}
    IN_dict = {"IN":IN_list}
    HK_dict = {"HK":HK_list}

    for loc_dict in [UK_dict, US_dict, IN_dict, HK_dict]:
        # searching for key terms of different dicts
        for loc in loc_dict.values()[0]:
            if len(loc)>0 and loc not in location:
                if loc in user_loc or loc.lower() in user_loc:
                    location.append(loc)
        # IF location recognised: merging key terms
        if len(location)>0:
            location = (",").join(location)
            # Adding general location
            output.append(loc_dict.keys()[0])
            break

    # IF location NOT recognised: labelling unknown as other
    if len(location)==0:
        # Adding general location
        output.append("-")
        location = "other"

    # Adding specific location
    output.append(location)
    logging.debug("specified location:")
    logging.debug(location)
    return output

# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):

    # Received data
    def on_success(self, data):

        # Only collect tweets in English
        if data['lang'] == 'en':
            logging.debug('processing tweet')
            logging.debug(data)
            tweet_data = process_tweet(data)
            logging.debug('write to spreadsheet')
            logging.info(tweet_data)
            try:
                self.write_to_googlesheet(tweet_data)
            except Exception as e:
                logging.error('ERROR Could not write to Google spreadsheet')
                logging.error(str(e))
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


logging.debug('starting stream')

while True:
    try:
        # Instantiate from our streaming class
        stream = MyStreamer(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'],
                            credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
        # Start the streamon', location='') # you can add location here for the ones related
        stream.statuses.filter(track='air pollution')
    except Exception as e:
        logging.error(e)
        continue