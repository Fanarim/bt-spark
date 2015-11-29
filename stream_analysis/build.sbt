name := "Test app"

version := "0.1"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.5.1",
	"org.apache.spark" %% "spark-streaming" % "1.5.1",
	"org.apache.spark" %% "spark-streaming-twitter" % "1.5.1",
	"org.twitter4j" % "twitter4j-core" % "3.0.3",
	"org.twitter4j" % "twitter4j-stream" % "3.0.3",
	"mysql" % "mysql-connector-java" % "5.1.+",
	"com.typesafe.slick" %% "slick" % "3.1.0"
)


resolvers ++= Seq(
	"Twitter4j" at "http://twitter4j.org/maven2/"
)
