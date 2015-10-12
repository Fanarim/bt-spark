import java.util.Date
import scala.collection.mutable.HashMap

import org.apache.log4j.Logger
import org.apache.log4j.Level
//import org.apache.hadoop.io.compress.DefaultCodec
import org.apache.spark.streaming._
import twitter4j._
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.streaming.twitter._

object TwitterDataCollector {
	def main(args: Array[String]){
		// setup level of messages that should be displayed in console
		Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
		Logger.getLogger("org.apache.spark.storage.BlockManager").setLevel(Level.WARN)

		//------------------------------------------------------------------------------------
		// To set following variables, set them up in the environment using export VARNAME=VAL
		// temporary local repository
		val tmpDir = sys.env.getOrElse("TMP_DIR", "/tmp").toString

		// output directory
		val outputDir = sys.env.getOrElse("OUTPUT_DIR", "/tmp/tweets_output")

		// batch interval in seconds
		val batchInterval = sys.env.get("BATCH_INTERVAL").map(_.toInt).getOrElse(60)

		// output files per batch
		val outputBatchFiles = sys.env.get("OUTPUT_BATCH_FILES").map(_.toInt).getOrElse(1)

		// print settings
		Seq(("TEMP DIR" -> tmpDir),
		    ("OUTPUT DIR" -> outputDir),
		    ("OUTPUT INTERVAL" -> batchInterval),
		    ("BATCH FILES PER INTERVAL" -> outputBatchFiles)).foreach {
			case (k, v) => println("%s: %s".format(k, v))
		} 

		// TODO - check batch interval (hive partitioning?? only supports 60 and 3600)

		//------------------------------------------------------------------------------------
		// setup Twitter
		// credentials
		val consumerKey = "vsFXbOa0zCGESXkArqe7GNKyA"
		val consumerSecret = "ZFFxOWOY4m8NVyoO9kQ4FcibDbhVw5gRf6f4kTmJJaXpSox7mb"
		val accessToken = "37232208-BsaG8JeNLPHaXcvaqqLO2RKImGTachmvFUpLClSrv"
		val accessTokenSecret = "me9G6RDhouDguDId0urGmMS7rs5J27bocm6T2yF6AC2Bw"

		val map = new HashMap[String, String]
		map ++= Map("consumerKey" -> consumerKey,
			    "consumerSecret" -> consumerSecret,
			    "accessToken" -> accessToken,
			    "accessTokenSecret" -> accessTokenSecret)
		val configKeys = Seq("consumerKey", "consumerSecret", "accessToken", "accessTokenSecret")

		// setup Twitter OAuth
		println("Setting up Twitter OAuth")
		configKeys.foreach(key => {
			if(!map.contains(key)) {
				throw new Exception("Error setting OAuth authentication - value for " + key + " not found")
			}
			val fullKey = "twitter4j.oauth." + key
			System.setProperty(fullKey, map(key))
			println("\tProperty " + fullKey + " set as " + map(key) + "\n")
		})
	
		//------------------------------------------------------------------------------------
	
				
	
		

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", (batchInterval * 5).toString)	
		System.setProperty("spark.cleaner.delay", (batchInterval * 5).toString)

		// set date format
		val hiveDateFormat = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss.0")
		val year = new java.text.SimpleDateFormat("yyyy")
		val month = new java.text.SimpleDateFormat("MM")
		val day = new java.text.SimpleDateFormat("dd")
		val hour = new java.text.SimpleDateFormat("HH")
		val minute = new java.text.SimpleDateFormat("mm")
		val second = new java.text.SimpleDateFormat("ss")
			
		// A list of fields we want along with Hive column names and data types
    		val fields: Seq[(Status => Any, String, String)] = Seq(
			(s => s.getId, "id", "BIGINT"),
			(s => s.getInReplyToStatusId, "reply_status_id", "BIGINT"),
			(s => s.getInReplyToUserId, "reply_user_id", "BIGINT"),
			(s => s.getRetweetCount, "retweet_count", "INT"),
			(s => s.getText, "text", "STRING"),
			(s => Option(s.getGeoLocation).map(_.getLatitude()).getOrElse(""), "latitude", "FLOAT"),
			(s => Option(s.getGeoLocation).map(_.getLongitude()).getOrElse(""), "longitude", "FLOAT"),
			(s => s.getSource, "source", "STRING"),
			(s => s.getUser.getId, "user_id", "INT"),
			(s => s.getUser.getName, "user_name", "STRING"),
			(s => s.getUser.getScreenName, "user_screen_name", "STRING"),
			(s => hiveDateFormat.format(s.getUser.getCreatedAt), "user_created_at", "TIMESTAMP"),
			(s => s.getUser.getFollowersCount, "user_followers", "BIGINT"),
			(s => s.getUser.getFavouritesCount, "user_favorites", "BIGINT"),
			(s => s.getUser.getLang, "user_language", "STRING"),
			(s => s.getUser.getLocation, "user_location", "STRING"),
			(s => s.getUser.getTimeZone, "user_timezone", "STRING"),

			// Break out date fields for partitioning
			(s => hiveDateFormat.format(s.getCreatedAt), "created_at", "TIMESTAMP"),
			(s => year.format(s.getCreatedAt), "created_at_year", "INT"),
			(s => month.format(s.getCreatedAt), "created_at_month", "INT"),
			(s => day.format(s.getCreatedAt), "created_at_day", "INT"),
			(s => hour.format(s.getCreatedAt), "created_at_hour", "INT"),
			(s => minute.format(s.getCreatedAt), "created_at_minute", "INT"),
			(s => second.format(s.getCreatedAt), "created_at_second", "INT")
		)
		
		// For making a table later, print out the schema
		val tableSchema = fields.map{case (f, name, hiveType) => "%s %s".format(name, hiveType)}.mkString("(", ", ", ")")
		println("Beginning collection. Table schema for Hive is: %s".format(tableSchema))

		// Remove special characters inside of statuses that screw up Hive's scanner.
		def formatStatus(s: Status): String = {
			def safeValue(a: Any) = Option(a)
				.map(_.toString)
				.map(_.replace("\t", ""))
				.map(_.replace("\"", ""))
				.map(_.replace("\n", ""))
				.map(_.replaceAll("[\\p{C}]","")) // Control characters
				.getOrElse("")	
	
			fields.map{case (f, name, hiveType) => f(s)}
				.map(f => safeValue(f))
				.mkString("\t")
		}
		
		// Date format for creating Hive partitions
		val outDateFormat = batchInterval match {
			case 60 => new java.text.SimpleDateFormat("yyyy/MM/dd/HH/mm")
			case 3600 => new java.text.SimpleDateFormat("yyyy/MM/dd/HH")
    		}

		
		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext("spark://10.0.2.15:7077", "Twitter Streaming", Seconds(30))
		val stream = TwitterUtils.createStream(ssc, None)

		
		
		//val tweets = ssc.twitterStream()

		// format each tweet
		//val formattedTweets = tweets.map(s => formatStatus(s))

		// group into larger batches
		//val batchedTweets = formattedTweets.window(Seconds(batchInterval), Seconds(batchInterval))

		// coalesce each batch into fixed number of files
		//val coalesced = batchedTweets.transform(rdd => rdd.coalesce(outputBatchFiles))

		// save to output directory
		//coalesced.foreach((rdd, time) => {
		//	val outPartitionFolder = outDateFormat.format(new Date(time.miliseconds))
		//	rdd.saveAsTextFile("%s%s".format(outputDir, outPartitionFolder), classOf[DefaultCodec])
		//})


		//------------------------------------------------------------------------------------
		// Start streaming
		//ssc.checkpoint(tmpDir)
		ssc.start()
		ssc.awaitTermination()
	}
}
