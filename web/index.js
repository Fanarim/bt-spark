var APIurl = 'http://twitter-wish-api.herokuapp.com/';

// create statsChart
var totalTweets = ['Total tweets']
var englishTweets = ['English tweets']
var wishes = ['Wishes']
var sentiment_average = ['Average sentiment']
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

var sentimentChart = c3.generate({
    bindto: '#sentimentChart',
    data: {
      x: 'times',
      xFormat: '%Y-%m-%d %H:%M:%S',
      columns: [
        sentiment_average,
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
