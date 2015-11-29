import java.util.Date
import scala.collection.mutable.HashMap

import org.apache.log4j.Logger
import org.apache.log4j.Level
//import org.apache.hadoop.io.compress.DefaultCodec
import org.apache.spark.streaming._
import twitter4j._
import org.apache.spark.SparkContext._
import org.apache.spark.streaming.twitter._

object TwitterDataCollector {
	def main(args: Array[String]){
		// setup level of messages that should be displayed in console
		Logger.getLogger("org.apache.spark").setLevel(Level.WARN)
		Logger.getLogger("org.apache.spark.storage.BlockManager").setLevel(Level.WARN)

		//------------------------------------------------------------------------------------
		// setup Twitter credentials
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
			// println("\tProperty " + fullKey + " set as " + map(key) + "\n")
		})

		//------------------------------------------------------------------------------------

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", "30")
		System.setProperty("spark.cleaner.delay", "30")

		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext("local[4]", "Twitter Streaming", Seconds(5)) // local[4] = compute localy, use 4 cores
		val stream = TwitterUtils.createStream(ssc, None) // None = default Twitter4j authentication method

		val hashTags = stream.flatMap(status => status.getText.split(" ").filter(_.startsWith("#")))

		val topCounts10 = hashTags.map((_, 1)).reduceByKeyAndWindow(_ + _, Seconds(30))
                     .map{case (topic, count) => (count, topic)}
                     .transform(_.sortByKey(false))

		topCounts10.foreachRDD(rdd => {
      			val topList = rdd.take(10)
		        println("\nPopular topics in last 30 seconds (%s total):".format(rdd.count()))
		        topList.foreach{case (count, tag) => println("%s (%s tweets)".format(tag, count))}
		})

		// val tweets = stream.map(status => status.getText())
		// tweets.saveAsTextFiles("/tmp/tweetlog/time", "tweetlog")
		//------------------------------------------------------------------------------------
		// Start streaming
		ssc.start()
		ssc.awaitTermination()
	}
}
