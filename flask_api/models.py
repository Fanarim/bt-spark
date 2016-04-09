from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()


tweet_mentions_user = db.Table(
    'tweet_mentions_user', db.Model.metadata,
    db.Column('tweet_id', db.BigInteger, db.ForeignKey('tweet_wishes.id')),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'))
)

tweet_contains_hashtag = db.Table(
    'tweet_contains_hashtag', db.Model.metadata,
    db.Column('tweet_id', db.BigInteger, db.ForeignKey('tweet_wishes.id')),
    db.Column('hashtag', db.String, db.ForeignKey('hashtags.hashtag'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String)
    profile_picture_url = db.Column(db.String)
    wishes = relationship("TweetWish",
                          back_populates="user")
    mentioned_in = relationship("TweetWish",
                                secondary=tweet_mentions_user,
                                back_populates="mentioned_users")

    def json_dump(self):
        return dict(id=self.id,
                    username=self.username,
                    profile_picture_url=self.profile_picture_url)


class TweetWish(db.Model):
    __tablename__ = 'tweet_wishes'
    id = db.Column(db.BigInteger, primary_key=True)
    author = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    tweet_text = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    is_retweet = db.Column(db.Boolean)
    retweet_tweet_id = db.Column(db.BigInteger)
    sentiment = db.Column(db.Float)
    user = relationship("User",
                        back_populates="wishes")
    mentioned_users = relationship("User",
                                   secondary=tweet_mentions_user,
                                   back_populates="mentioned_in")
    hashtags = relationship("Hashtag",
                            secondary=tweet_contains_hashtag,
                            back_populates="contained_in")

    def json_dump(self):
        return dict(id=self.id,
                    author=self.author,
                    tweet_text=self.tweet_text.replace("&quot;", "\""),
                    created_at=str(self.created_at),
                    is_retweet=self.is_retweet,
                    retweet_tweet_id=self.retweet_tweet_id,
                    sentiment=self.sentiment)


class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    hashtag = db.Column(db.String, primary_key=True)
    contained_in = relationship("TweetWish",
                                secondary=tweet_contains_hashtag,
                                back_populates="hashtags")

    def json_dump(self):
            return dict(hashtag=self.hashtag)


class Stats3s(db.Model):
    __tablename__ = 'stats_general_3s'
    datetime = db.Column(db.DateTime, primary_key=True)
    tweets_total = db.Column(db.Integer)
    tweets_english = db.Column(db.Integer)
    wishes_total = db.Column(db.Integer)
    sentiment_average = db.Column(db.Float)

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
    sentiment_average = db.Column(db.Float)

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
    sentiment_average = db.Column(db.Float)

    def json_dump(self):
        return dict(datetime=str(self.datetime),
                    tweets_total=self.tweets_total,
                    tweets_english=self.tweets_english,
                    wishes_total=self.wishes_total,
                    sentiment_average=self.sentiment_average)
