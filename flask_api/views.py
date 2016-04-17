import time
import json

from flask import request, jsonify
from flask.ext.restless import ProcessingException
from sqlalchemy.sql import func
from sqlalchemy import desc

from main import app
from models import *


def check_valid_arguments(arguments, allowed_arguments):
    for arg in arguments:
        if arg not in allowed_arguments:
            raise ProcessingException(description='Invalid argument: ' + arg,
                                      code=400)


def validate_and_set_interval(arguments):
    time_now = time.time()
    time_from = (time_now - 60 * 10)
    time_to = time_now

    if 'from' in arguments:
        try:
            float(arguments['from'])
        except:
            raise ProcessingException(
                description='Invalid value in "from" parameter',
                code=400)
        time_from = arguments['from']

    if 'to' in arguments:
        try:
            float(arguments['to'])
        except:
            raise ProcessingException(
                description='Invalid value in "to" parameter',
                code=400)
        time_to = arguments['to']

    return time_from, time_to


# return wishes from last 10 minutes by default or from chosen interval
@app.route('/wish/', methods=['GET'])
def wishes():
    check_valid_arguments(request.args, ["to", "from", "count"])
    time_from, time_to = validate_and_set_interval(request.args)

    if 'count' in request.args:
        wishes = TweetWish.query\
            .order_by(TweetWish.created_at.desc())\
            .limit(request.args['count'])
    else:
        wishes = TweetWish.query\
            .filter(func.unix_timestamp(TweetWish.created_at) < time_to)\
            .filter(func.unix_timestamp(TweetWish.created_at) >= time_from)\
            .order_by(TweetWish.created_at.desc())
    return jsonify(wishes=[item.json_dump() for item in wishes])


# return wish with specified id
@app.route('/wish/<wish_id>/', methods=['GET'])
def wish(wish_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)
    wish = TweetWish.query\
        .get_or_404(wish_id)
    return jsonify(wish.json_dump())


# return users mentioned in wish with given id
@app.route('/wish/<wish_id>/mentions/', methods=['GET'])
def wish_mentions(wish_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    mentioned_users = TweetWish.query\
        .get_or_404(wish_id)\
        .mentioned_users
    return jsonify(
        mentioned_users=[item.json_dump() for item in mentioned_users])


# return hashtags contained in wish with given id
@app.route('/wish/<wish_id>/hashtags/', methods=['GET'])
def wish_hashtags(wish_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    hashtags = TweetWish.query\
        .get_or_404(wish_id)\
        .hashtags
    return jsonify(hashtags=[item.hashtag for item in hashtags])


# return all users
@app.route('/user/', methods=['GET'])
def users():
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    users = User.query\
        .order_by(User.id.asc())
    return jsonify(users=[item.json_dump() for item in users])


# return user with specified id
@app.route('/user/<user_id>/', methods=['GET'])
def user(user_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    user = User.query\
        .get_or_404(user_id)
    return jsonify(user.json_dump())


# return user's tweets
@app.route('/user/<user_id>/wishes/', methods=['GET'])
def user_wishes(user_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    wishes = User.query\
        .get_or_404(user_id)\
        .wishes
    return jsonify(wishes=[item.json_dump() for item in wishes])


# return user's mentions
@app.route('/user/<user_id>/mentioned_in/', methods=['GET'])
def user_mentioned_in(user_id):
    if len(request.args) != 0:
        raise ProcessingException(
            description='Invalid argument provided',
            code=400)

    wishes = User.query\
        .get_or_404(user_id)\
        .mentioned_in
    return jsonify(wishes=[item.json_dump() for item in wishes])


# return hashtags used in given interval and their count.
# Results are sorted by this count descending
@app.route('/stats/hashtags/', methods=['GET'])
def hashtag_stats():
    check_valid_arguments(request.args, ["to", "from", "count"])
    time_from, time_to = validate_and_set_interval(request.args)

    if 'count' in request.args:
        hashtags = TweetWish\
            .query\
            .join(tweet_contains_hashtag)\
            .join(Hashtag)\
            .with_entities(Hashtag.hashtag)\
            .add_column(func.count(Hashtag.hashtag))\
            .group_by(Hashtag.hashtag)\
            .order_by(desc(func.count(Hashtag.hashtag)))\
            .limit(request.args['count'])\
            .all()
    else:
        hashtags = TweetWish\
            .query\
            .filter(func.unix_timestamp(TweetWish.created_at) < time_to)\
            .filter(func.unix_timestamp(TweetWish.created_at) >= time_from)\
            .join(tweet_contains_hashtag)\
            .join(Hashtag)\
            .with_entities(Hashtag.hashtag)\
            .add_column(func.count(Hashtag.hashtag))\
            .group_by(Hashtag.hashtag)\
            .order_by(desc(func.count(Hashtag.hashtag)))\
            .all()

    return jsonify(
        popular_hashtags=[{'hashtag': key, 'count': value} for key, value in hashtags])


# return mentions in given interval and their count.
# Results are sorted by this count descending
@app.route('/stats/mentions/', methods=['GET'])
def mention_stats():
    check_valid_arguments(request.args, ["to", "from", "count"])
    time_from, time_to = validate_and_set_interval(request.args)

    if 'count' in request.args:
        mentions = User\
            .query\
            .join(tweet_mentions_user)\
            .join(TweetWish)\
            .add_column(func.count(User.id))\
            .group_by(User.id)\
            .order_by(desc(func.count(User.id)))\
            .limit(request.args['count'])\
            .all()
    else:
        mentions = User\
            .query\
            .join(tweet_mentions_user)\
            .join(TweetWish)\
            .filter(func.unix_timestamp(TweetWish.created_at) < time_to)\
            .filter(func.unix_timestamp(TweetWish.created_at) >= time_from)\
            .add_column(func.count(User.id))\
            .group_by(User.id)\
            .order_by(desc(func.count(User.id)))\

    serialized = []
    for result in mentions:
        serialized.append({'user': result[0].json_dump(),
                           'mention_count': result[1]})
    return jsonify(popular_users=serialized)


# manual endpoint - stats history endpoint
@app.route('/stats/general/', methods=['GET'])
def stats_history():
    check_valid_arguments(request.args, ["to", "from", "density"])
    time_from, time_to = validate_and_set_interval(request.args)
    if 'density' in request.args:
        if request.args['density'] in ["3s", "10m", "1d"]:
            time_density = request.args['density']
        else:
            raise ProcessingException(
                description='Invalid value for "density" parameter',
                code=400)
    else:
            time_density = "3s"
    if time_density == "3s":
        stats = Stats3s.query\
            .filter(func.unix_timestamp(Stats3s.datetime) < time_to)\
            .filter(func.unix_timestamp(Stats3s.datetime) >= time_from)
    if time_density == "10m":
        stats = Stats10m.query\
            .filter(func.unix_timestamp(Stats10m.datetime) < time_to)\
            .filter(func.unix_timestamp(Stats10m.datetime) >= time_from)
    if time_density == "1d":
        stats = Stats1d.query\
            .filter(func.unix_timestamp(Stats1d.datetime) < time_to)\
            .filter(func.unix_timestamp(Stats1d.datetime) >= time_from)

    serialized = [item.json_dump() for item in stats]
    return jsonify(stats=serialized)


# return wishes containing selcted hashtag
@app.route('/hashtag/<hashtag>/wishes/', methods=['GET'])
def hahtag_wishes(hashtag):
    check_valid_arguments(request.args, [])

    wishes = TweetWish\
        .query\
        .join(tweet_contains_hashtag)\
        .join(Hashtag)\
        .filter(Hashtag.hashtag == hashtag)

    return jsonify(wishes=[item.json_dump() for item in wishes])
