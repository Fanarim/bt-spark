#!/usr/bin/env python3.4

from flask import Flask, abort, request
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True
db = SQLAlchemy(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

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


# manual endpoint
@app.route('/wishes/', methods = ['GET'])
def index():
    wishes = TweetWish.query.all()
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({ 'wishes': serialized })

# automatic endpoint
manager.create_api(TweetWish, methods=['GET'], results_per_page=-1)

if __name__ == '__main__':
    app.run()
