city = "London"

var settings = {
  "async": true,
  "crossDomain": true,
  "url": "https://api.openaq.org/v1/measurements"+"?city="+city+"&limit="+"1"+"&parameter=pm25",
  "method": "GET",
  "headers": {}
}

$.ajax(settings).done(function (response) {
  console.log(response);
});


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