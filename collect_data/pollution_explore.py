import requests

url_countries = "http://api.airvisual.com/v2/countries"
url_states = "http://api.airvisual.com/v2/states"
url_cities = "http://api.airvisual.com/v2/cities"
pollution_api_key = "ahQ3grN738QipJk7A"

querystring = {"key":pollution_api_key}

response = requests.request("GET", url_countries, params=querystring)

print(response.text)
print(len(response.json()["data"]))

querystring = {"country":"USA","key":pollution_api_key}
response = requests.request("GET", url_states, params=querystring)

print(response.text)
print(len(response.json()["data"]))

querystring = {"state":"Hong Kong", "country":"Hong Kong", "key":pollution_api_key}
response = requests.request("GET", url_cities, params=querystring)

print(response.text)
print(len(response.json()["data"]))