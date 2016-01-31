Repository for storing data related to my bachelor thesis.



Available API endpoints:

http://twitter-wish-api.herokuapp.com/last_wishes

- last 10 wishes


http://twitter-wish-api.herokuapp.com/wishes

- all wishes


http://twitter-wish-api.herokuapp.com/api/tweet_wishes

- all wishes


http://twitter-wish-api.herokuapp.com/stats/?from=[timestamp]&to=[timestamp]&density=[density]

- stats - number of tweets, english tweets and wishes in given time interval.

-- All parameters are optional. [timestamp] is classic unix timestamp. Only available option for density right now is "3s".



For example API usage, see http://tweet-wishes.s3-website.eu-central-1.amazonaws.com/
