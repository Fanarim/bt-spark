var APIurl = 'http://twitter-wish-api.herokuapp.com/';
var weburl = 'http://tweetwishes.com/';
var userId = location.search.split('id=')[1]

$.getJSON( APIurl + 'user/' + userId + '/', function(data)
  {
    var user = data;
    document.getElementById('tweet_author').innerHTML = '<a href=' + weburl +
      'user.html?id=' + user.id + '><h3>' +
      user.username + '</h3></a>';
    document.getElementById('tweet_image').innerHTML = '<img width=120px src="' + user.profile_picture_url + '"/>';
    document.getElementById('username').innerHTML = user.username;
  }
);

$.getJSON( APIurl + 'user/' + userId + '/wishes', function(data)
  {
    var tweets = data.wishes;
    for (i = 0; i < tweets.length; i++) {
      if (tweets[i].sentiment == 2){
        document.getElementById('tweet_list').innerHTML += '<div class="well neutral"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment <= 1) {
        document.getElementById('tweet_list').innerHTML += '<div class="well negativenegative"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment >= 3) {
        document.getElementById('tweet_list').innerHTML += '<div class="well positivepositive"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment > 2) {
        document.getElementById('tweet_list').innerHTML += '<div class="well positive"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment < 2) {
        document.getElementById('tweet_list').innerHTML += '<div class="well negative"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else {
        document.getElementById('tweet_list').innerHTML += '<div class="well neutral"><a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      }
    }
  }
);

$.getJSON( APIurl + 'user/' + userId + '/mentioned_in', function(data)
  {
    var tweets = data.wishes;
    for (i = 0; i < tweets.length; i++) {
      if (tweets[i].sentiment == 2){
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well neutral"><a href="' + weburl + '/user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment <= 1) {
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well negativenegative"><a href="' + weburl + 'user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment >= 3) {
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well positivepositive"><a href="' + weburl + 'user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment > 2) {
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well positive"><a href="' + weburl + 'user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else if (tweets[i].sentiment < 2) {
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well negative"><a href="' + weburl + 'user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      } else {
        document.getElementById('mentioned_in_tweets').innerHTML += '<div class="well neutral"><a href="' + weburl + 'user.html?id=' +
          tweets[i].author.id + '"><strong>' +
          tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
      }
    }
  }
);
