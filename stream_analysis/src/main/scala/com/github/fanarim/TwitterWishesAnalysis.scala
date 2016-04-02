package com.github.fanarim

import java.util.Date
import scala.collection.mutable._
import org.apache.log4j.Logger
import org.apache.log4j.Level
import org.apache.spark.streaming._
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.streaming.twitter._
import org.apache.spark.sql._
import twitter4j._
import scala.io.Source
import java.util.Calendar
import java.util.TimeZone
import java.text.SimpleDateFormat

object TwitterWishesAnalysis {
	def main(args: Array[String]){
		// setup level of messages that should be displayed in console
		Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
		Logger.getLogger("org.apache.spark.storage.BlockManager").setLevel(Level.ERROR)

		// setup spark
		val conf = new SparkConf().setAppName("Twitter Wishes Analysis")
		val sc = new SparkContext(conf)

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
		val configKeys = Seq("consumerKey", "consumerSecret", "accessToken",
			"accessTokenSecret")

		// setup Twitter OAuth
		println("Setting up Twitter OAuth")
		configKeys.foreach(key => {
			if(!map.contains(key)) {
				throw new Exception("Error setting OAuth authentication - value for "	+
				  key + " not found")
			}
			val fullKey = "twitter4j.oauth." + key
			System.setProperty(fullKey, map(key))
		})

		// setup DB
		val DBUrl = "jdbc:mysql://" + dbPath + "/" + dbName + "?user=" + dbUser +
		  "&password=" + dbPass
		val prop = new java.util.Properties
		prop.setProperty("driver", "com.mysql.jdbc.Driver")

		//------------------------------------------------------------------------------------

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", "5")
		System.setProperty("spark.cleaner.delay", "5")
		System.setProperty("spark.executor.memory","4g")
		System.setProperty("spark.driver.memory","4g")

		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext(sc, Seconds(3))
		// None = default Twitter4j authentication method
		val stream = TwitterUtils.createStream(ssc, None)

		var tweetCount = 0L
		var tweetCountEnglish = 0L
		var wishCount = 0L

		// count tweets
		stream.count().foreachRDD( rdd => {
			tweetCount = rdd.first()
		})

		// filter English tweets and count them
		var tweetWishesStream = stream.filter( status => ( status.getLang() == "en"))
		tweetWishesStream.count().foreachRDD ( rdd => {
			tweetCountEnglish = rdd.first()
		})

		// filter wishes and count them
		tweetWishesStream = tweetWishesStream
			.filter( status => (
				status.getText().contains("wish") ||
				status.getText().contains("hope") ||
				status.getText().contains("pray") ))
		tweetWishesStream.count().foreachRDD( rdd => {
			wishCount = rdd.first()
		})

		tweetWishesStream.foreachRDD{rdd =>
			// get current datetime
			val timestampFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
			timestampFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
			val currentDatetime = timestampFormat.format(Calendar.getInstance().getTime())

			// print wishes to STDOUT
			rdd.foreach{status =>
				println("ID: " +
					status.getId() +
					"\nUSER: " +
					status.getUser().getName() +
				  "\nTWEET: " +
					status.getText() +
					"\nRETWEETED: " +
					status.isRetweet() +
					"\n\n")
			}

			// create dataframe containg users TODO include mentioned users
			val authors_saved = ssqlc.read.jdbc(DBUrl, "users", prop).registerTempTable("users")
			val authors_current = rdd.map(status =>
				{
					(status.getUser().getId(),
						status.getUser().getName(),
						status.getUser().getBiggerProfileImageURL())
				})
				.toDF("id",
					"username",
					"profile_picture_url")

			// filter only users that are not already saved
			val authors_current_array = authors_current.distinct().collect()
			var authors_new: collection.mutable.Seq[(Long, String, String)] = collection.mutable.Seq()
			for(author_current <- authors_current_array){
				if (ssqlc.sql("SELECT * FROM users WHERE id = " + author_current(0)).count() == 0){
					authors_new = authors_new :+ (author_current(0).asInstanceOf[Long],
						author_current(1).asInstanceOf[String],
						author_current(2).asInstanceOf[String])
				}
			}
			// convert new users to DF and write to DB
			val authors_new_df = ssqlc.createDataFrame(authors_new).toDF("id", "username", "profile_picture_url")
			authors_new_df.write.mode(SaveMode.Append).jdbc(DBUrl, "users", prop)

			// create dataframe containing wishes
			val wishes_df = rdd.map(status =>
				{
					// get ID of original tweet if this is retweet, otherwise set own ID
					var retweet_tweet_id = 0L
					if(status.isRetweet()){
						retweet_tweet_id = status.getRetweetedStatus().getId()
					} else {
						retweet_tweet_id = status.getId()
					}

					// return tuple with tweet details
		      (status.getId(),
						status.getUser().getId(),
						status.getText(),
						timestampFormat.format(status.getCreatedAt()),
						status.isRetweet(),
						retweet_tweet_id,
						0);
				}) // convert RDD to DF
				.toDF("id",
					"author",
					"tweet_text",
					"created_at",
					"is_retweet",
					"retweet_tweet_id",
					"sentiment")

			// write wishes to DB
			wishes_df.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_wishes", prop)

			// write stats to DB
			val stats = ssqlc.createDataFrame(Seq((currentDatetime, tweetCount,
				tweetCountEnglish, wishCount, 0)))
				.toDF("datetime",
					"tweets_total",
					"tweets_english",
					"wishes_total",
					"sentiment_average")
			stats.write.mode(SaveMode.Append).jdbc(DBUrl, "stats_general_3s", prop)
		}

		//------------------------------------------------------------------------------------
		// Start streaming
		ssc.start()
		ssc.awaitTermination()
	}
}
