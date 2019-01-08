import requests

url_countries = "http://api.airvisual.com/v2/countries"
url_states = "http://api.airvisual.com/v2/states"
url_cities = "http://api.airvisual.com/v2/cities"
pollution_api_key = "ahQ3grN738QipJk7A"

querystring = {"key":pollution_api_key}

response = requests.request("GET", url_countries, params=querystring)

print(response.text)
print(len(response.json()["data"]))

def find_states(country):
    querystring = {"country":country,"key":pollution_api_key}
    response = requests.request("GET", url_states, params=querystring)
    list = []
    print(response.json()["data"])
    for dict in response.json()["data"]:
        print(dict["state"])
        list.append(dict["state"])
    return(list)

def get_cities_list(criteria):
    '''
        List criteria [*country* <string>, *state* <string>]
        returns list of lists of locations with specified city
    '''
    # get cities from api
    querystring = {"state": criteria[0], "country": criteria[1], "key": pollution_api_key}
    response = requests.request("GET", url_cities, params=querystring)

    # construct list
    output_list = []
    for dict in response.json()["data"]:
        output_list.append([dict["city"], criteria[0], criteria[1]])

    return output_list


find_states("United Kingdom")
# get_cities_list(["United Kingdom", "England"])