var APIurl = 'http://twitter-wish-api.herokuapp.com/';
var weburl = 'http://tweetwishes.com/';
var hashtag = location.search.split('id=')[1]

document.getElementById('hashtag').innerHTML = hashtag;

$.getJSON( APIurl + 'hashtag/' + hashtag + '/wishes', function(data)
{
  var tweets = data.wishes;
  for (i = 0; i < tweets.length; i++) {
    if (tweets[i].sentiment == 2){
      document.getElementById('tweet_list').innerHTML += '<div class="well neutral"><a href="' + weburl + '/user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    } else if (tweets[i].sentiment <= 1) {
      document.getElementById('tweet_list').innerHTML += '<div class="well negativenegative"><a href="' + weburl + 'user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    } else if (tweets[i].sentiment >= 3) {
      document.getElementById('tweet_list').innerHTML += '<div class="well positivepositive"><a href="' + weburl + 'user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    } else if (tweets[i].sentiment > 2) {
      document.getElementById('tweet_list').innerHTML += '<div class="well positive"><a href="' + weburl + 'user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    } else if (tweets[i].sentiment < 2) {
      document.getElementById('tweet_list').innerHTML += '<div class="well negative"><a href="' + weburl + 'user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    } else {
      document.getElementById('tweet_list').innerHTML += '<div class="well neutral"><a href="' + weburl + 'user.html?id=' +
        tweets[i].author.id + '"><strong>' +
        tweets[i].author.username + '</a></strong>:<a href=' + weburl + 'wish.html?id=' + tweets[i].id + ">" + tweets[i].tweet_text + "</a></div>";
    }
  }
}
);
