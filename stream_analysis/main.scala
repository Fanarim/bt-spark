import java.util.Date
import scala.collection.mutable.HashMap
import org.apache.log4j.Logger
import org.apache.log4j.Level
import org.apache.spark.streaming._
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.streaming.twitter._
import org.apache.spark.sql._
import twitter4j._
import scala.io.Source

object TwitterDataCollector {
	def main(args: Array[String]){
		// setup level of messages that should be displayed in console
		Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
		Logger.getLogger("org.apache.spark.storage.BlockManager").setLevel(Level.ERROR)

		// setup spark
		val sc = new SparkContext("local[2]", "Stream analysis Twitter")

		val ssqlc = new SQLContext(sc)
		import ssqlc.implicits._


		//------------------------------------------------------------------------------------
		// setup Twitter credentials
		val twitterLines = Source.fromFile("../twitter_cred.txt").getLines.toArray
		val twitterConsumerKey = twitterLines(0)
		val twitterConsumerSecret = twitterLines(1)
		val twitterAccessToken = twitterLines(2)
		val twitterAccessTokenSecret = twitterLines(3)

		// read database credentials
		val dbLines = Source.fromFile("../db_cred.txt").getLines.toArray
		val dbPath = dbLines(0)
		val dbName = dbLines(1)
		val dbUser = dbLines(2)
		val dbPass = dbLines(3)

		val map = new HashMap[String, String]
		map ++= Map("consumerKey" -> twitterConsumerKey,
			    "consumerSecret" -> twitterConsumerSecret,
			    "accessToken" -> twitterAccessToken,
			    "accessTokenSecret" -> twitterAccessTokenSecret)
		val configKeys = Seq("consumerKey", "consumerSecret", "accessToken", "accessTokenSecret")

		// setup Twitter OAuth
		println("Setting up Twitter OAuth")
		configKeys.foreach(key => {
			if(!map.contains(key)) {
				throw new Exception("Error setting OAuth authentication - value for " + key + " not found")
			}
			val fullKey = "twitter4j.oauth." + key
			System.setProperty(fullKey, map(key))
		})

		// setup DB
		val DBUrl = "jdbc:mysql://" + dbPath + "/" + dbName + "?user=" + dbUser + "&password=" + dbPass
		val prop = new java.util.Properties
		prop.setProperty("driver", "com.mysql.jdbc.Driver")

		//------------------------------------------------------------------------------------

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", "30")
		System.setProperty("spark.cleaner.delay", "30")

		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext(sc, Seconds(2)) // local[4] = compute localy, use 4 cores
		val stream = TwitterUtils.createStream(ssc, None) // None = default Twitter4j authentication method

		var tweetCount = 0L
		var tweetCountNew = 0L
		var wishCount = 0L

		val tweetWishesStream = stream
			.filter( status => ( status.getText().contains("wish") || status.getText().contains("hope") || status.getText().contains("pray") ))
			.filter( status => ( status.getLang() == "en"))

		stream.count().foreachRDD( rdd => { tweetCount += rdd.first() })
		stream.count().foreachRDD( rdd => {	tweetCountNew = rdd.first() })
		tweetWishesStream.count().foreachRDD( rdd => { wishCount += rdd.first() })

		// print wishes and save them to db
		tweetWishesStream.foreachRDD{rdd =>
			// printing only wishes processed on master, the others are printed to client's stdout?
			rdd.foreach{status =>
				println("ID: " + status.getId() + "\nUSER: " + status.getUser().getName() + "\nTWEET: " +
				status.getText() + "\nRETWEETED: " + status.isRetweet() + "\n\n")
			}
			val wishes_df = rdd.map(status =>
	                        (status.getId(), status.getUser().getName(), status.getText(), status.isRetweet())
                        	).toDF("id", "username", "tweet", "is_retweet")
			wishes_df.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_wishes", prop)
			println(wishCount + " wishes out of " + tweetCount + " (" + tweetCountNew + " new)" + " total tweets. ")
		}

		//------------------------------------------------------------------------------------
		// Start streaming
		ssc.start()
		ssc.awaitTermination()
	}
}
