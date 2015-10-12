name := "Test app"

version := "0.1"

scalaVersion := "2.10.4"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.4.0",
	"org.apache.spark" %% "spark-streaming" % "1.4.0",
	"org.apache.spark" %% "spark-streaming-twitter" % "1.4.0",
	"org.twitter4j" % "twitter4j-core" % "3.0.3",
	"org.twitter4j" % "twitter4j-stream" % "3.0.3"
)


resolvers ++= Seq(
	"Twitter4j" at "http://twitter4j.org/maven2/"
)
