import requests
from google_sheet import enter_pollution
from datetime import datetime, timedelta
import time
import logging

logging.basicConfig(filename='pollution_crawler.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

#https://docs.openaq.org/#api-Measurements
class PollutionData:
    def __init__(self, city):
        self.url = "https://api.openaq.org/v1/measurements"
        self.city = city
        self.date_time = self.query_date_time()
        self.date = self.date_time[:10]
        self.time = self.date_time[11:-1]
        self.pm25 = self.query_values("pm25")
        self.pm10 = self.query_values("pm10")
        self.no2 = self.query_values("no2")
        self.o3 = self.query_values("o3")
        self.co = self.query_values("co")

        logging.info([self.date_time, self.date, self.time, self.city, self.pm25, self.pm10, self.no2, self.o3, self.co])

    # Query search
    def query_values(self, parameter):
        querystring = {"city": self.city, "limit": 1, "parameter": parameter}
        response = requests.request("GET", self.url, params=querystring)
        try:
            return response.json()['results'][0]['value']
        except:
            return ""

    def query_date_time(self):
        querystring = {"city": self.city, "limit": 1}
        response = requests.request("GET", self.url, params=querystring)
        return response.json()['results'][0]['date']['utc']

def query_cities (country):
    querystring = {"country": country, "limit": 20}
    response = requests.request("GET", "https://api.openaq.org/v1/cities", params=querystring)
    print(response.json())

def query_countries ():
    response = requests.request("GET", "https://api.openaq.org/v1/countries")
    print(response.json())


location_list = ["London", "Birmingham", "Manchester", "Leeds", "Edinburgh","Glasgow", "Swansea", "Plymouth",
                 "New York-Northern New Jersey-Long Island", "Minneapolis-St. Paul-Bloomington", "MONTEZUMA","Detroit-Warren-Livonia",
                 "Cleveland-Elyria-Mentor", "Mumbai", "Delhi", "Central","Kowloon","New Territories","Causeway Bay"]

while True:
    dt = datetime.now() + timedelta(hours=1)
    print
    for loc in location_list:
        try:
            data = PollutionData(loc)
            row = [str(i) for i in [data.date_time, data.date, data.time, data.city, data.pm25, data.pm10, data.no2, data.o3, data.co]]
            enter_pollution(row)
        except Exception as e:
            print loc, str(e)
            logging.error(str(e))
            dt = datetime.now()
            break

    while datetime.now() < dt:
        time.sleep(1)
