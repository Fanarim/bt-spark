import time
import json

from flask import request, jsonify
from flask.ext.restless import ProcessingException
from sqlalchemy.sql import func

from main import app
from models import *


# return wishes from last 10 minutes by default or from chosen interval
@app.route('/wish/', methods=['GET'])
def wishes():
    for arg in request.args:
        if arg not in ["to", "from"]:
            raise ProcessingException(description='Invalid argument: ' + arg,
                                      code=400)
    time_now = time.time()
    time_from = (time_now - 60 * 10)
    time_to = time_now

    if 'from' in request.args:
        try:
            float(request.args['from'])
        except:
            raise ProcessingException(
                description='Invalid value in "from" parameter',
                code=400)
        time_from = request.args['from']

    if 'to' in request.args:
        try:
            float(request.args['to'])
        except:
            raise ProcessingException(
                description='Invalid value in "to" parameter',
                code=400)
        time_to = request.args['to']

    wishes = TweetWish.query\
        .filter(func.unix_timestamp(TweetWish.created_at) < time_to)\
        .filter(func.unix_timestamp(TweetWish.created_at) >= time_from)\
        .order_by(TweetWish.created_at.desc())
    return jsonify(wishes=[item.json_dump() for item in wishes])


# return wish with specified id
@app.route('/wish/<tweet_id>', methods=['GET'])
def wish(tweet_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)
    wish = TweetWish.query\
        .get_or_404(tweet_id)
    return jsonify(wish.json_dump())


# manual endpoint - get last 10 tweets
@app.route('/last_wishes/', methods=['GET'])
def last_tweets():
    wishes = TweetWish.query.order_by('id desc').limit(10)
    serialized = [item.json_dump() for item in wishes]
    return json.dumps({'wishes': serialized})


# manual endpoint - stats history endpoint
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
        if request.args['density'] in ["3s", "10m", "1d"]:
            history_density = request.args['density']
        else:
            pass
            # TODO invalid parameter
    if history_density == "3s":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats3s.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats3s.datetime) >= history_from)
    if history_density == "10m":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats10m.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats10m.datetime) >= history_from)
    if history_density == "1d":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats1d.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats1d.datetime) >= history_from)

    serialized = [item.json_dump() for item in stats]
    return json.dumps({'stats': serialized})


# manual endpoint - single tweet with given id
# TODO return also hashtags, mentioned user, number of retweets recorded, ...
@app.route('/wish', methods=['GET'])
def wish_detail():
    if 'id' in request.args and request.args['id'].isnumeric():
        wish_id = request.args['id']
    else:
        # TODO error, no tweet id given
        pass
    wish = TweetWish.query.filter(TweetWish.id == wish_id)
    try:
        serialized = wish[0].json_dump()
        return json.dumps(serialized)
    # no wish found
    except:
        # TODO
        pass
