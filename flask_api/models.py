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
    db.Column('hashtag', db.String(140), db.ForeignKey('hashtags.hashtag'))
)


class User(db.Model):
    def __init__(self, id, username, profile_picture_url):
        self.id = id
        self.username = username
        self.profile_picture_url = profile_picture_url

    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(140))
    profile_picture_url = db.Column(db.Text)
    wishes = relationship("TweetWish",
                          back_populates="user")
    mentioned_in = relationship("TweetWish",
                                secondary=tweet_mentions_user,
                                lazy='dynamic',
                                back_populates="mentioned_users")

    def json_dump(self):
        return dict(id=str(self.id),
                    username=self.username,
                    profile_picture_url=self.profile_picture_url)


class TweetWish(db.Model):
    def __init__(self,
                 id,
                 author,
                 tweet_text,
                 created_at,
                 is_retweet,
                 retweet_tweet_id,
                 sentiment):
        self.id = id
        self.author = author
        self.tweet_text = tweet_text
        self.created_at = created_at
        self.is_retweet = is_retweet
        self.retweet_tweet_id = retweet_tweet_id
        self.sentiment = sentiment

    __tablename__ = 'tweet_wishes'
    id = db.Column(db.BigInteger, primary_key=True)
    author = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    tweet_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    is_retweet = db.Column(db.Boolean)
    retweet_tweet_id = db.Column(db.BigInteger)
    sentiment = db.Column(db.Float)
    user = relationship("User",
                        back_populates="wishes")
    mentioned_users = relationship("User",
                                   secondary=tweet_mentions_user,
                                   lazy='dynamic',
                                   back_populates="mentioned_in")
    hashtags = relationship("Hashtag",
                            secondary=tweet_contains_hashtag,
                            lazy='dynamic',
                            back_populates="contained_in")

    def json_dump(self):
        return dict(id=str(self.id),
                    author=self.user.json_dump(),
                    tweet_text=self.tweet_text.replace("&quot;", "\""),
                    created_at=str(self.created_at),
                    is_retweet=self.is_retweet,
                    retweet_tweet_id=str(self.retweet_tweet_id),
                    sentiment=self.sentiment)


class Hashtag(db.Model):
    def __init__(self, hashtag):
        self.hashtag = hashtag

    __tablename__ = 'hashtags'
    hashtag = db.Column(db.String(140), primary_key=True)
    contained_in = relationship("TweetWish",
                                secondary=tweet_contains_hashtag,
                                lazy='dynamic',
                                back_populates="hashtags")

    def json_dump(self):
            return dict(hashtag=self.hashtag)


class Stats3s(db.Model):
    def __init__(self,
                 datetime,
                 tweets_total,
                 tweets_english,
                 wishes_total,
                 sentiment_average):
        self.datetime = datetime
        self.tweets_total = tweets_total
        self.tweets_english = tweets_english
        self.wishes_total = wishes_total
        self.sentiment_average = sentiment_average

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
    def __init__(self,
                 datetime,
                 tweets_total,
                 tweets_english,
                 wishes_total,
                 sentiment_average):
        self.datetime = datetime
        self.tweets_total = tweets_total
        self.tweets_english = tweets_english
        self.wishes_total = wishes_total
        self.sentiment_average = sentiment_average

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
    def __init__(self,
                 datetime,
                 tweets_total,
                 tweets_english,
                 wishes_total,
                 sentiment_average):
        self.datetime = datetime
        self.tweets_total = tweets_total
        self.tweets_english = tweets_english
        self.wishes_total = wishes_total
        self.sentiment_average = sentiment_average

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
