// Calculating London AQI
var help = document.getElementById("help");
var help_hide = document.getElementById("help-hide");

$(document).ready(function(){ 
	help.style.display = "none"
}) 


function place_change(city){
	console.log("place change to "+city)
	var values_dict = {};
	
	if (["London", "Birmingham", "Manchester"].includes(city)) {
		console.log("UK mean!")
		var mean_dict = {
			"pm25": 11.5147,
			"pm10": 17.0046,
			"o3": 33.1524,
			"no2": 29.9907,
		}
		pollutants = ["pm25","pm10","o3","no2"]
	} else {
		var mean_dict = {
			"pm25": 194.827,
			"pm10": 175.279,
			"o3": 53.297,
			"no2": 28.094,
			"co": 1542.049
		}
		pollutants = ["pm25","pm10","o3","no2", "co"]
	}
	
	var IAQI_dict = {}

	function api_get(city, parameter){
		var settings = {
		  "async": false,
		  "crossDomain": true,
		  "url": "https://api.openaq.org/v1/measurements"+"?city="+city+"&limit="+"1"+"&parameter="+parameter,
		  "method": "GET",
		  "headers": {}
		}

		$.ajax(settings).done(function (response) {
		  console.log(response);
		  values_dict[parameter] = response["results"][0]["value"]
		});
	}
	
	for (var i in pollutants){
		try{
			console.log(city, pollutants[i]);
			api_get(city, pollutants[i])
		}catch(e){
			console.log(e)
		}
	}
	

	for (var key in values_dict) {
		// check if the property/key is defined in the object itself, not in parent
		IAQI_dict[key] = values_dict[key]/mean_dict[key] *100
	}

	var max_value = 0;
	var max_key;

	for (var key in IAQI_dict) {
	  if(IAQI_dict[key] > max_value) {
		max_value = IAQI_dict[key];
		max_key = key;
	  }
	}

	max_value = Math.round( max_value * 10 ) / 10;
	care_value = Math.round(Math.random()*130);
	max_diff = max_value*0.3
	potential_value = Math.round((max_value-max_diff*(care_value/130))*10)/10;



	// Setting to site
	function set_lung(image_id, value){
		if (value<51){
			document.getElementById(image_id).src = "media/lung1.gif";
		} else if (value>50 && value<101) {
			document.getElementById(image_id).src = "media/lung2.gif";
		} else if (value>100 && value<151){
			document.getElementById(image_id).src = "media/lung3.gif";
		} else if (value>150 && value<201){
			document.getElementById(image_id).src = "media/lung4.gif";
		} else if (value>200 && value<301){
			document.getElementById(image_id).src = "media/lung5.gif";
		} else {
			document.getElementById(image_id).src = "media/lung6.gif";
		}
	}

	function set_care_lung(image_id, value){
		if (value<21){
			document.getElementById(image_id).src = "media/care1.gif";
		} else if (value>20 && value<41) {
			document.getElementById(image_id).src = "media/care2.gif";
		} else if (value>40 && value<61){
			document.getElementById(image_id).src = "media/care3.gif";
		} else if (value>60 && value<81){
			document.getElementById(image_id).src = "media/care4.gif";
		} else if (value>80 && value<91){
			document.getElementById(image_id).src = "media/care5.gif";
		} else {
			document.getElementById(image_id).src = "media/care6.gif";
		}
	}

	document.getElementById("ldn_aqi").innerHTML = max_value.toString()
	set_lung("aqi_lung", max_value)
	document.getElementById("ldn_potential").innerHTML = potential_value.toString()
	set_lung("potential_lung", potential_value)
	document.getElementById("ldn_care").innerHTML = care_value.toString()
	set_care_lung("care_lung", care_value)
}

function reply_click(clicked_id)
{	
	help.style.display = "none"
	help_hide.style.display = "block"
    place_change(clicked_id);
	
}

function show_help(clicked_id)
{
	var help = document.getElementById("help");
    help.style.display = "block"
	help_hide.style.display = "none"
}


//location_list = ["London", "Birmingham", "Manchester", "Leeds", "Edinburgh","Glasgow", "Swansea", "Plymouth",
//                 "New York-Northern New Jersey-Long Island", "Minneapolis-St. Paul-Bloomington", "MONTEZUMA","Detroit-Warren-Livonia",
//                 "Cleveland-Elyria-Mentor", "Mumbai", "Delhi", "Central","Kowloon","New Territories","Causeway Bay"]
/* var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://stream.twitter.com/1.1/statuses/filter.json?track=air",
  "method": "GET",
  "headers": { 
	consumer_key: consumer_secret,
	access_token: access_secret
  }
}
$.ajax(settings).done(function (response) {
  console.log(response);
});

$.ajax({
	type: 'GET',
	url: "https://api.twitter.com/1.1/search/tweets.json?q=airpollution",
	headers: twitter_cred,
	success: function(data){
		console.log(data)
	}
}) */