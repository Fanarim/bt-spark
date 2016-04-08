
from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy()


class TweetWishes(db.Model):
    __tablename__ = 'tweet_wishes'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    tweet_text = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    is_retweet = db.Column(db.Boolean)
    retweet_tweet_id = db.Column(db.Integer)
    sentiment = db.Column(db.Integer)

    def json_dump(self):
        return dict(id=self.id,
                    author=self.author,
                    tweet_text=self.tweet_text.replace("&quot;", "\""),
                    created_at=str(self.created_at),
                    is_retweet=self.is_retweet,
                    retweet_tweet_id=self.retweet_tweet_id,
                    sentiment=self.sentiment)


class Stats3s(db.Model):
    __tablename__ = 'stats_general_3s'
    datetime = db.Column(db.DateTime, primary_key=True)
    tweets_total = db.Column(db.Integer)
    tweets_english = db.Column(db.Integer)
    wishes_total = db.Column(db.Integer)
    sentiment_average = db.Column(db.Integer)

    def json_dump(self):
        return dict(datetime=str(self.datetime),
                    tweets_total=self.tweets_total,
                    tweets_english=self.tweets_english,
                    wishes_total=self.wishes_total,
                    sentiment_average=self.sentiment_average)


class Stats10m(db.Model):
    __tablename__ = 'stats_general_10m'
    datetime = db.Column(db.DateTime, primary_key=True)
    tweets_total = db.Column(db.Integer)
    tweets_english = db.Column(db.Integer)
    wishes_total = db.Column(db.Integer)
    sentiment_average = db.Column(db.Integer)

    def json_dump(self):
        return dict(datetime=str(self.datetime),
                    tweets_total=self.tweets_total,
                    tweets_english=self.tweets_english,
                    wishes_total=self.wishes_total,
                    sentiment_average=self.sentiment_average)


class Stats1d(db.Model):
    __tablename__ = 'stats_general_1d'
    datetime = db.Column(db.DateTime, primary_key=True)
    tweets_total = db.Column(db.Integer)
    tweets_english = db.Column(db.Integer)
    wishes_total = db.Column(db.Integer)
    sentiment_average = db.Column(db.Integer)

    def json_dump(self):
        return dict(datetime=str(self.datetime),
                    tweets_total=self.tweets_total,
                    tweets_english=self.tweets_english,
                    wishes_total=self.wishes_total,
                    sentiment_average=self.sentiment_average)
