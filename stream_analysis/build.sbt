name := "Tweets_stream_analysis"

version := "0.1"

scalaVersion := "2.10.6"

mergeStrategy in assembly <<= (mergeStrategy in assembly) { (old) =>
   {
    case PathList("META-INF", xs @ _*) => MergeStrategy.discard
    case x => MergeStrategy.first
   }
}

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.6.1" % "provided",
	"org.apache.spark" %% "spark-streaming" % "1.6.1" % "provided",
	"org.apache.spark" %% "spark-streaming-twitter" % "1.6.1",
	"org.apache.spark" %% "spark-sql" % "1.6.1" % "provided",
	"org.twitter4j" % "twitter4j-core" % "4.0.4",
	"org.twitter4j" % "twitter4j-stream" % "4.0.4",
	"mysql" % "mysql-connector-java" % "5.1.38",
  "edu.stanford.nlp" % "stanford-corenlp" % "3.6.0",
  "edu.stanford.nlp" % "stanford-corenlp" % "3.6.0" classifier "models"
)


resolvers ++= Seq(
	"Twitter4j" at "http://twitter4j.org/maven2/"
)
