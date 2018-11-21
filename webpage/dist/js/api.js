var pollution_api_key = "ahQ3grN738QipJk7A"

//variables
var city = "Los Angeles"
var state = "California"
var country = "USA"

// process
city = city.replace(" ","%20");
console.log(city)

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://api.airvisual.com/v2/city?city="+city+"&state="+state+"&country="+country+"&key="+pollution_api_key,
  "method": "GET",
  "headers": {}
}

$.ajax(settings).done(function (response) {
  console.log(response);
});

var twitter_api_key = "HPo1fKvKHLBjfNgQMzAvWMmnU"
var twitter_api_secret_key = "tXLfD3tGqf3QiGFhIu7GiPJ3w0gtZeaJdqNl815bxQVrcbD9y1"
var twitter_access_token = "75251127-mx4Ywt3edUQmmzhG44MinpirrCSA4BecA2H8PXOXb"
var twitter_access_token_secret = "dZGTs5oyCIU2Z2HEXX1sOwdQLlUjYqTfRO3jzgoYUKryU"

