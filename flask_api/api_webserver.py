#!/usr/bin/env python3.4

from flask import Flask, abort, request
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True
db = SQLAlchemy(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

# Setup CORS to allow javascript clients process the data from API
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # allow accesing this from any source
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

class TweetWish(db.Model):
    __tablename__ = 'tweet_wishes'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    tweet = db.Column(db.String)
    is_retweet = db.Column(db.Boolean)

    # manual serialization
    def json_dump(self):
        return dict(id = self.id,
                    username = self.username,
                    tweet = self.tweet.replace("&quot;", "\""),
                    is_retweet = self.is_retweet)


# manual endpoint - all tweets
@app.route('/wishes/', methods = ['GET'])
def index():
    wishes = TweetWish.query.all()
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({ 'wishes': serialized })

# manual endpoint - get last 10 tweets
@app.route('/last_wishes/', methods = ['GET'])
def last_tweets():
    wishes = TweetWish.query.order_by('id desc').limit(10)
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({ 'wishes': serialized })

# automatic endpoint
manager.create_api(TweetWish, methods=['GET'], results_per_page=-1)
app.after_request(add_cors_headers)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
