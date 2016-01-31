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
  getStats();
}, 3000);


function getLastWishes() {
  $.getJSON( APIurl + 'last_wishes', function(data)
    {
      var tweets = data.wishes;
      for (i = 0; i < 6; i++) {
        document.getElementById('last_tweet_' + i).innerHTML = "<strong>" +
          tweets[i].username + ": </strong>" + tweets[i].tweet;
      }
    }
  );
}


function getStats() {
  // get data from API
  $.getJSON(APIurl + 'stats', function(data){
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
