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
import org.apache.spark.sql.functions.mean
import twitter4j._
import scala.io.Source
import java.util.Calendar
import java.util.TimeZone
import java.text.SimpleDateFormat
import com.github.fanarim.sentiment.SentimentAnalysis._

object TwitterWishesAnalysis {
	def main(args: Array[String]){
		// setup level of messages that should be displayed in console
		Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
		Logger.getLogger("org.apache.spark.storage.BlockManager").setLevel(Level.ERROR)

		// set TLS version to prevent "SSL peer shut down incorrectly" error
		System.setProperty("https.protocols", "TLSv1.1");

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
		  "&password=" + dbPass + "&charset=utf8mb4"
		val prop = new java.util.Properties
		prop.setProperty("driver", "com.mysql.jdbc.Driver")

		//------------------------------------------------------------------------------------

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", "50")
		System.setProperty("spark.cleaner.delay", "50")
		System.setProperty("spark.executor.memory","8g")
		System.setProperty("spark.driver.memory","8g")

		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext(sc, Seconds(40))
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

			ssqlc.read.jdbc(DBUrl, "users", prop).registerTempTable("users")
			ssqlc.cacheTable("users")
			ssqlc.read.jdbc(DBUrl, "hashtags", prop).registerTempTable("hashtags")
			ssqlc.cacheTable("hashtags")
			ssqlc.read.jdbc(DBUrl, "tweet_wishes", prop).registerTempTable("tweet_wishes")
			ssqlc.cacheTable("tweet_wishes")

			// create dataframe containg tweet authors
			val authors_current = rdd.map(status =>
				{
					(status.getUser().getId(),
						status.getUser().getName(),
						status.getUser().getBiggerProfileImageURL())
				})
				.toDF("id",
					"username",
					"profile_picture_url")

			// create dataframe containing tweetId and information about mentioned users
			var mentioned_current_rdd = rdd.flatMap(status =>
				{
					var tweet_mention_entities = status.getUserMentionEntities()
					for(entity <- tweet_mention_entities) yield {
						(status.getId(), entity.getId(), entity.getName(), "")
					}
				}
			)
			val mentioned_current = mentioned_current_rdd.collect()
				.toSeq
				.toDF("tweet_id", "id", "username", "profile_picture_url")

			val mentioned_current_users = mentioned_current.select("id", "username", "profile_picture_url")
			val mentioned_current_relations = mentioned_current.select("tweet_id" ,"id")

			// join dataframe with tweet authors and mentioned users
			val users_current = authors_current.unionAll(mentioned_current_users)

			// filter only users that are not already saved
			val users_current_array = users_current.dropDuplicates(Seq("id")).collect()
			var users_new: collection.mutable.Seq[(Long, String, String)] = collection.mutable.Seq()
			for(user_current <- users_current_array){
				if (ssqlc.sql("SELECT * FROM users WHERE id = " + user_current(0)).count() == 0){
					users_new = users_new :+ (user_current(0).asInstanceOf[Long],
						user_current(1).asInstanceOf[String],
						user_current(2).asInstanceOf[String])
				}
			}
			// convert new users to DF and write to DB
			val users_new_df = ssqlc.createDataFrame(users_new).toDF("id", "username", "profile_picture_url")
			users_new_df.write.mode(SaveMode.Append).jdbc(DBUrl, "users", prop)

			// create dataframe containing hashtags used
			var hashtags_current_rdd = rdd.flatMap(status =>
				{
					var tweet_hashtag_entities = status.getHashtagEntities()
					for(entity <- tweet_hashtag_entities) yield {
						Tuple2(status.getId(), entity.getText())
					}
				}
			)
			val hashtags_current_relations = hashtags_current_rdd.collect()
				.toSeq
				.toDF("tweet_id", "hashtag")

			val hashtags_current = hashtags_current_relations.select("hashtag")

			// filter only hashtags that are not already saved
			val hashtags_current_array = hashtags_current.distinct().collect()

			var hashtags_new: collection.mutable.Seq[Tuple1[(String)]] = collection.mutable.Seq()
			for(hashtag_current <- hashtags_current_array){
				if (ssqlc.sql("SELECT * FROM hashtags WHERE hashtag=\""
						+ hashtag_current(0).asInstanceOf[String].toLowerCase()
						+ "\"").count() == 0){
					// check hashtag isn't already included in hashtags_new
					if ( !hashtags_new.contains(Tuple1(hashtag_current(0).asInstanceOf[String].toLowerCase()))){
						hashtags_new = hashtags_new :+ Tuple1(hashtag_current(0).asInstanceOf[String].toLowerCase())
					}
				}
			}

			// convert new hashtags to DF and write to DB
			val hashtags_new_df = ssqlc.createDataFrame(hashtags_new).toDF("hashtag")
			hashtags_new_df.write.mode(SaveMode.Append).jdbc(DBUrl, "hashtags", prop)

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
						getAverageSentiment(status.getText()));
				}) // convert RDD to DF
				.toDF("id",
					"author",
					"tweet_text",
					"created_at",
					"is_retweet",
					"retweet_tweet_id",
					"sentiment")

			// write wishes to DB
			wishes_df.distinct.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_wishes", prop)

			// save tweet_mentions_user data to DB
			mentioned_current_relations.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_mentions_user", prop)

			// save tweet_contains_hashtag data to DB
			hashtags_current_relations.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_contains_hashtag", prop)

			val average_sentiment_arr = wishes_df.select(mean("sentiment")).collect()
			var average_sentiment = average_sentiment_arr(0).get(0).asInstanceOf[Double]

			if(average_sentiment == 0){
				average_sentiment = 2
			}

			// write stats to DB
			val stats = ssqlc.createDataFrame(Seq((currentDatetime, tweetCount,
				tweetCountEnglish, wishCount, average_sentiment)))
				.toDF("datetime",
					"tweets_total",
					"tweets_english",
					"wishes_total",
					"sentiment_average")
			stats.write.mode(SaveMode.Append).jdbc(DBUrl, "stats_general_40s", prop)
		}

		//------------------------------------------------------------------------------------
		// Start streaming
		ssc.start()
		ssc.awaitTermination()
	}
}
