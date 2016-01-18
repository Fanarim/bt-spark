name := "Test app"

version := "0.1"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.6.0",
	"org.apache.spark" %% "spark-streaming" % "1.6.0",
	"org.apache.spark" %% "spark-streaming-twitter" % "1.6.0",
	"org.apache.spark" %% "spark-sql" % "1.6.0",
	"org.twitter4j" % "twitter4j-core" % "4.0.4",
	"org.twitter4j" % "twitter4j-stream" % "4.0.4",
	"mysql" % "mysql-connector-java" % "5.1.+"
)


resolvers ++= Seq(
	"Twitter4j" at "http://twitter4j.org/maven2/"
)
