var APIurl = 'http://twitter-wish-api.herokuapp.com/';
var webUrl = 'http://tweet-wishes.s3-website.eu-central-1.amazonaws.com/';
var tweetId = location.search.split('id=')[1]

$.getJSON( APIurl + 'wish?id=' + tweetId, function(data)
  {
    var tweet = data;
    document.getElementById('tweet_id').innerHTML = tweet.id;
    document.getElementById('tweet_created_at').innerHTML = tweet.created_at;
    document.getElementById('tweet_author').innerHTML = tweet.author;
    document.getElementById('tweet_text').innerHTML = tweet.tweet_text;
    document.getElementById('tweet_retweeted').innerHTML = "<a href=" + webUrl +
      "wish.html?id=" + tweet.retweet_tweet_id + ">" + tweet.retweet_tweet_id + "</a>";
  }
);
