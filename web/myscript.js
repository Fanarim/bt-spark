var APIurl = 'http://twitter-wish-api.herokuapp.com/';

// create statsChart
var totalTweets = ['Total tweets']
var englishTweets = ['English tweets']
var wishes = ['Wishes']
var times = ['times']
var statsChart = c3.generate({
    bindto: '#statsChart',
    data: {
      x: 'times',
      xFormat: '%Y-%m-%d %H:%M:%S',
      columns: [
        totalTweets,
        englishTweets,
        wishes,
        times
      ]
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%H:%M:%S'
            }
        }
    }
});

getLastWishes();
getStats();

window.setInterval(function(){
  getLastWishes();
  getPopularHashtags();
  getPopularMentions();
  getStats();
}, 7500);


function getLastWishes() {
  $.getJSON( APIurl + 'wish/?count=6', function(data)
    {
      var tweets = data.wishes;
      for (i = 0; i < 6; i++) {
        document.getElementById('last_tweet_' + i).innerHTML = "<strong>" +
          tweets[i].author.username + ": </strong>" + tweets[i].tweet_text;
        if (tweets[i].sentiment == 2){
          document.getElementById('last_tweet_' + i).parentNode.className = "well neutral"
        } else if (tweets[i].sentiment <= 1) {
          document.getElementById('last_tweet_' + i).parentNode.className = "well negativenegative"
        } else if (tweets[i].sentiment >= 3) {
          document.getElementById('last_tweet_' + i).parentNode.className = "well positivepositive"
        } else if (tweets[i].sentiment > 2) {
          document.getElementById('last_tweet_' + i).parentNode.className = "well positive"
        } else if (tweets[i].sentiment < 2) {
          document.getElementById('last_tweet_' + i).parentNode.className = "well negative"
        } else {
          document.getElementById('last_tweet_' + i).parentNode.className = "well neutral"
        }
      }
    }
  );
}


function getStats() {
  // get data from API
  $.getJSON(APIurl + 'stats/general', function(data){
    var stats = data.stats;
    totalTweets = ['Total tweets'];
    englishTweets = ['English tweets'];
    wishes = ['Wishes'];
    times = ['times'];
    for (i = 0; i < stats.length; i++){
      totalTweets.push(stats[i].tweets_total);
      englishTweets.push(stats[i].tweets_english);
      wishes.push(stats[i].wishes_total);
      times.push(stats[i].datetime);
    }
  });
  statsChart.load({
    columns: [
      totalTweets,
      englishTweets,
      wishes,
      times,
    ],
    type: 'line'
  });
}

function getPopularHashtags() {
  $.getJSON( APIurl + 'stats/hashtags?count=6', function(data)
    {
      var hashtags = data.popular_hashtags;
      for (i = 0; i < 6; i++) {
        document.getElementById('popular_hashtag_' + i).innerHTML = "<strong>" +
          hashtags[i].hashtag + "</strong>";
          document.getElementById('popular_hashtag_count_' + i).innerHTML = hashtags[i].count;
      }
    }
  );
}

function getPopularMentions() {
  $.getJSON( APIurl + 'stats/mentions?count=6', function(data)
    {
      var mentions = data.popular_users;
      for (i = 0; i < 6; i++) {
        document.getElementById('popular_mention_' + i).innerHTML = "<strong>" +
          mentions[i].user.username + "</strong>";
          document.getElementById('popular_mention_count_' + i).innerHTML = mentions[i].mention_count;
      }
    }
  );
}
