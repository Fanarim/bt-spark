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
		})

		// setup DB
		val DBUrl = "jdbc:mysql://localhost:3306/spark_streaming?user=root&password=root"
		val prop = new java.util.Properties
		prop.setProperty("driver", "com.mysql.jdbc.Driver")

		//------------------------------------------------------------------------------------

		// enable meta-data cleaning in Spark so that this program can run forever
		System.setProperty("spark.cleaner.tt1", "30")
		System.setProperty("spark.cleaner.delay", "30")

		//------------------------------------------------------------------------------------
		// Spark stream setup
		// new Twitter stream
		val ssc = new StreamingContext(sc, Seconds(3)) // local[4] = compute localy, use 4 cores
		val stream = TwitterUtils.createStream(ssc, None) // None = default Twitter4j authentication method

		val tweetWishesStream = stream.map(status => status)
			.filter( status => ( status.getText().contains("wish") || status.getText().contains("hope")))
			// .filter( status => ( status.getLang() == "ENGLISH")) // Twitter4j 4.0.4 only, spark using older version for now, but upgrade is planned

		// print wishes and save them to db
		tweetWishesStream.foreach{rdd =>
			rdd.foreach{status =>
				println("ID: " + status.getId() + "\nUSER: " + status.getUser().getName() + "\nTWEET: " +
				status.getText() + "\nRETWEETED: " + status.isRetweet() + "\n\n")
			}
			val wishes_df = rdd.map(status =>
	                        (status.getId(), status.getUser().getName(), status.getText(), status.isRetweet())
                        	).toDF("id", "username", "tweet", "is_retweet")
			wishes_df.write.mode(SaveMode.Append).jdbc(DBUrl, "tweet_wishes", prop)
		}

		//------------------------------------------------------------------------------------
		// Start streaming
		ssc.start()
		ssc.awaitTermination()
	}
}
