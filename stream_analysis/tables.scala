import slick.driver.MySQLDriver.api._

class TweetWishes(tag: Tag) extends Table[(Int, String, String, Boolean)](tag, "tweet_wishes") {
  def id = column[Int]("id")
  def username = column[String]("username")
  def tweet = column[String]("tweet")
  def isRetweet = column[Boolean]("is_retweet")

  // Every table needs a * projection with the same type as the table's type parameter
  def * = (id, username, tweet, isRetweet)
}
