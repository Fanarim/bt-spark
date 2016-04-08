import time
import json


from flask import request
from sqlalchemy.sql import func

from main import app
from models import *


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
            .filter(func.unix_timestamp(Stats3s.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats3s.datetime) >= history_from)
    if history_density == "1d":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats3s.datetime) < history_to)\
            .filter(func.unix_timestamp(Stats3s.datetime) >= history_from)

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
    wish = TweetWishes.query.filter(TweetWishes.id == wish_id)
    try:
        serialized = wish[0].json_dump()
        return json.dumps(serialized)
    # no wish found
    except:
        # TODO
        pass
