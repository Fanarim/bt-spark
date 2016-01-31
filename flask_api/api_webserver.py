#!/usr/bin/env python3.4

from flask import Flask, abort, request
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json
import os
import time

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True
db = SQLAlchemy(app)

manager = APIManager(app, flask_sqlalchemy_db=db)


# Setup CORS to allow javascript clients process the data from API
def add_cors_headers(response):
    # allow accesing this from any source
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


class TweetWishes(db.Model):
    __tablename__ = 'tweet_wishes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    tweet = db.Column(db.String)
    is_retweet = db.Column(db.Boolean)

    def json_dump(self):
        return dict(id=self.id,
                    username=self.username,
                    tweet=self.tweet.replace("&quot;", "\""),
                    is_retweet=self.is_retweet)


class Stats3s(db.Model):
    __tablename__ = 'stats_3s'
    datetime = db.Column(db.DateTime, primary_key=True)
    tweets_total = db.Column(db.Integer)
    tweets_english = db.Column(db.Integer)
    wishes_total = db.Column(db.Integer)

    def json_dump(self):
        return dict(datetime=str(self.datetime),
                    tweets_total=self.tweets_total,
                    tweets_english=self.tweets_english,
                    wishes_total=self.wishes_total)


# manual endpoint - all tweets
@app.route('/wishes/', methods=['GET'])
def index():
    wishes = TweetWishes.query.all()
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({'wishes': serialized})


# manual endpoint - get last 10 tweets
@app.route('/last_wishes/', methods=['GET'])
def last_tweets():
    wishes = TweetWishes.query.order_by('id desc').limit(10)
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({'wishes': serialized})


# stats history endpoint
@app.route('/stats/', methods=['GET'])
def stats_history():
    time_now = time.time()
    history_from = (time_now - 60 * 10)
    history_to = time_now
    history_density = "3s"
    if 'from' in request.args:
        history_from = request.args['from']
    if 'to' in request.args:
        history_to = request.args['to']
    if 'density' in request.args:
        if request.args['density'] in ["3s", ]:
            history_density = request.args['density']
        else:
            pass
            # TODO invalid parameter
    if history_density == "3s":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats3s.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats3s.datetime) >= history_from)

    serialized = [item.json_dump() for item in stats]
    return json.dumps({'stats': serialized})


# automatic endpoint
manager.create_api(TweetWishes, methods=['GET'], results_per_page=-1)
app.after_request(add_cors_headers)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
