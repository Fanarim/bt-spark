// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});

// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

var APIurl = 'http://127.0.0.1:5000/';

getLastWishes();

window.setInterval(function(){
  getLastWishes();
}, 1000);

function getLastWishes() {
  $.getJSON( APIurl + 'last_wishes', function(data)
    {
      var tweets = data.wishes;
      // console.log(tweets);
      for (i = 0; i < 6; i++) {
        document.getElementById('last_tweet_' + i).innerHTML = "<strong>" + tweets[i].username + ": </strong>" + tweets[i].tweet;
      }
    }
  );
}

function drawChart() {
  // Create the data table.
  var data = new google.visualization.DataTable();
  data.addColumn('string', 'Topping');
  data.addColumn('number', 'Slices');
  data.addRows([
    ['Mushrooms', 3],
    ['Onions', 1],
    ['Olives', 1],
    ['Zucchini', 1],
    ['Pepperoni', 2]
  ]);

  // Set chart options
  var options = {'title':'How Much Pizza I Ate Last Night',
                 'titleTextStyle': {color: 'black', fontName: 'Arial', fontSize: '18', fontWidth: 'normal'},
                 'width':700,
                 'height':550,
                 'legend':'top',
                 'forceIFrame':'false'};

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
  chart.draw(data, options);
}
