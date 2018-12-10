import requests
import csv
import time
from google_sheet import enter_pollution
pollution_api_key = "ahQ3grN738QipJk7A"


def get_pollution_data(location):
    '''
        List specifying location [*city* <string>, *state* <string>, *country* <string>]
        returns json of pollution data
    '''
    url_city = "http://api.airvisual.com/v2/city"
    # get pollution info from api
    querystring = {"city":location[0],"state":location[1],"country":location[2],"key":pollution_api_key}
    response = requests.request("GET", url_city, params=querystring)
    print(response.json()['data'])
    data_p = response.json()['data']['current']['pollution']
    data = [data_p['ts'], data_p['aqicn'], data_p['aqius']]
    time.sleep(10)
    return data

def write_data(data, csv_name):
    '''
        API Response <json>, csv name <string>
        Writes info into csv file
    '''
    with open(csv_name + ".csv", 'a') as file:
        writer = csv.writer(file)
        print(data)
        writer.writerow(data)

def get_cities_list(criteria):
    '''
        List criteria [*country* <string>, *state* <string>]
        returns list of lists of locations with specified city
    '''
    # get cities from api
    url_cities = "http://api.airvisual.com/v2/cities"
    querystring = {"state": criteria[0], "country": criteria[1], "key": pollution_api_key}
    response = requests.request("GET", url_cities, params=querystring)

    # construct list
    output_list = []
    for dict in response.json()["data"]:
        output_list.append([dict["city"], criteria[0], criteria[1]])

    return output_list

### starting main code ###

# list of locations
location_list = [["London", "England","UK"], ["Birmingham", "England","UK"], ["Manchester", "England","UK"], ["Leeds", "England","UK"],
                 ["Edinburgh", "Scotland","UK"], ["Glasgow", "Scotland","UK"], ["Swansea", "Wales","UK"], ["Plymouth", "England","UK"],
                 ["Los Angeles", "California", "USA"], ["Beaumont", "Texas", "USA"], ["Orlando","Florida","USA"], ["Chicago","Illinois","USA"], ["Atlanta","Georgia","USA"],
                 ["Hamamachi","Kyoto","Japan"], ["Chiyoda", "Tokyo","Japan"], ["Ao","Osaka", "Japan"],
                 ["Delhi","Delhi","India"], ["New Delhi","Delhi","India"],
                 ["Hong Kong","Hong Kong","Hong Kong"]]

# loop through location
for location in location_list:
    print(location)
    # IF city specified
    if len(location)==3:
        print("data+writing")
        data = get_pollution_data(location)
        # write_data(data, "_".join(location))
        enter_pollution([','.join(location)] + data)

    # IF city not specified
    else:
        print("getting list")
        list = get_cities_list(location)
        print("list gotten", len(list))
        print(list)
        # get average of pollution
        total = [0, 0]
        for city in list:
            data = get_pollution_data(city)
            total[0] += int(data[1])
            total[1] += int(data[2])
        num = len(list)
        total_data = [','.join(location), data[0], total[0]/num, total[1]/num]
        # write_data(total_data, "_".join(location))
        enter_pollution(total_data)

