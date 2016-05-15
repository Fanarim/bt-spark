var APIurl = 'http://twitter-wish-api.herokuapp.com/';
var weburl = 'http://tweetwishes.com/';
var tweetId = location.search.split('id=')[1]

$.getJSON( APIurl + 'wish/' + tweetId + '/', function(data)
  {
    var tweet = data;
    document.getElementById('tweet_id').innerHTML = tweet.id;
    document.getElementById('tweet_created_at').innerHTML = tweet.created_at;
    document.getElementById('tweet_author').innerHTML = '<a href=' + weburl +
      'user.html?id=' + tweet.author.id + '><h3>' +
      tweet.author.username + '</h3></a>';
    document.getElementById('tweet_image').innerHTML = '<img width=120px src="' + tweet.author.profile_picture_url + '"/>'
    document.getElementById('tweet_text').innerHTML = tweet.tweet_text;

    if (tweet.sentiment == 2){
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary neutral">NEUTRAL</span>'
    } else if (tweet.sentiment <= 1) {
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary negativenegative">VERY NEGATIVE</span>'
    } else if (tweet.sentiment >= 3) {
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary positivepositive">VERY POSITIVE</span>'
    } else if (tweet.sentiment > 2) {
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary positive">POSITIVE</span>'
    } else if (tweet.sentiment < 2) {
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary negative">NEGATIVE</span>'
    } else {
      document.getElementById('tweet_text').innerHTML  += ' <span class="label label-primary neutral">NEUTRAL</span>'
    }
  }
);

$.getJSON( APIurl + 'wish/' + tweetId + '/hashtags/', function(data)
  {
    var hashtags = data.hashtags;
    for (i = 0; i < hashtags.length; i++) {
      document.getElementById('tweet_contains_hashtags').innerHTML  += ' <a href="' + weburl + 'hashtag.html?id=' + hashtags[i].hashtag + '"><span class="label label-success">#' + hashtags[i].hashtag + '</span></a>'
    }
  }
);

$.getJSON( APIurl + 'wish/' + tweetId + '/mentions/', function(data)
  {
    var mentions = data.mentioned_users;
    for (i = 0; i < mentions.length; i++) {
      document.getElementById('tweet_contains_mentions').innerHTML  += ' <a href="' + weburl + 'user.html?id=' + mentions[i].id + '"><span class="label label-primary">@' + mentions[i].username + '</span></a>'
    }
  }
);
