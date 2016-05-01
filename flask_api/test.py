#!/usr/bin/env python3

from flask.ext.testing import TestCase
from sqlalchemy import text
from wish_api import *

import datetime
import json
import time
import unittest


class UnitTesting(TestCase):
    def create_app(self):
        app.config.from_pyfile('config_test.py')
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        return app

    def setUp(self):
        time_now = time.time()

        db.drop_all()
        db.create_all()

        db.session.add(Hashtag("niceday"))
        db.session.add(Hashtag("old"))
        db.session.add(Hashtag("birthday"))

        db.session.add(User(123, "Jack", "http://profile.picture.url"))
        db.session.add(User(1414, "John", "http://profile.picture.url"))
        db.session.add(User(63774456, "Charles", "http://profile.picture.url"))

        db.session.add(TweetWish(889977,
                                 123,
                                 "I hope you have a #niceday, @john!",
                                 datetime.datetime.utcfromtimestamp(time_now - 60),
                                 False,
                                 889977,
                                 3.0))

        db.session.add(TweetWish(889999,
                                 63774456,
                                 "RT @jack: I hope you have a #niceday, @john!",
                                 datetime.datetime.utcfromtimestamp(time_now - 40),
                                 True,
                                 889977,
                                 3.0))

        db.session.add(TweetWish(93496545,
                                 123,
                                 "I wish I was younger. #old #birthday",
                                 datetime.datetime.utcfromtimestamp(time_now),
                                 False,
                                 93496545,
                                 1.0))

        db.session.commit()

        db.session.execute(
            text('INSERT INTO tweet_contains_hashtag VALUES (889977, "niceday");'))
        db.session.execute(
            text('INSERT INTO tweet_contains_hashtag VALUES (889999, "niceday");'))
        db.session.execute(
            text('INSERT INTO tweet_contains_hashtag VALUES (93496545, "old");'))
        db.session.execute(
            text('INSERT INTO tweet_contains_hashtag VALUES (93496545, "birthday");'))

        db.session.execute(
            text('INSERT INTO tweet_mentions_user VALUES (889977, 1414);'))
        db.session.execute(
            text('INSERT INTO tweet_mentions_user VALUES (889999, 1414);'))

        db.session.add(Stats3s(datetime.datetime.utcfromtimestamp(time_now - 20), 164, 19, 0, 2))
        db.session.add(Stats3s(datetime.datetime.utcfromtimestamp(time_now - 17), 184, 22, 1, 1.58))
        db.session.add(Stats3s(datetime.datetime.utcfromtimestamp(time_now - 14), 156, 24, 2, 3.45))
        db.session.add(Stats3s(datetime.datetime.utcfromtimestamp(time_now - 11), 175, 27, 0, 2))

        db.session.add(Stats10m(datetime.datetime.utcfromtimestamp(time_now - 2400), 32045, 8262, 152, 1.86))
        db.session.add(Stats10m(datetime.datetime.utcfromtimestamp(time_now - 1800), 34105, 8451, 121, 1.58))
        db.session.add(Stats10m(datetime.datetime.utcfromtimestamp(time_now - 1200), 18812, 9571, 114, 2.45))
        db.session.add(Stats10m(datetime.datetime.utcfromtimestamp(time_now - 600), 28411, 8225, 163, 2.25))

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_wish_list(self):
        time_now = time.time()

        response = self.client.get('/wish/', query_string={})
        assert response.status_code == 200
        assert len(response.json['wishes']) == 3

    def test_wish_list_interval(self):
        time_now = time.time()

        response = self.client.get('/wish/', query_string={'from': time_now - 10,
                                                           'to': time_now})
        assert response.status_code == 200
        wishes = {'wishes': [
            {'tweet_text': 'I wish I was younger. #old #birthday',
             'sentiment': 1.0,
             'created_at': '',
             'author': {'username': 'Jack',
                        'profile_picture_url': 'http://profile.picture.url',
                        'id': '123'},
             'retweet_tweet_id': '93496545',
             'id': '93496545',
             'is_retweet': False}]}
        response.json['wishes'][0]['created_at'] = ''
        self.assertEqual(response.json, wishes)

    def test_wish_list_count(self):
        time_now = time.time()

        response = self.client.get('/wish/', query_string={'count': 2})
        assert response.status_code == 200
        assert len(response.json['wishes']) == 2

    def test_wish_list_count_invalid(self):
        time_now = time.time()

        response = self.client.get('/wish/', query_string={'count': 'invalid'})
        assert response.status_code == 400

    def test_wish_detail(self):
        response = self.client.get('/wish/889977/', query_string={})
        assert response.status_code == 200
        wish = {'sentiment': 3.0,
                'tweet_text': 'I hope you have a #niceday, @john!',
                'created_at': '',
                'is_retweet': False,
                'retweet_tweet_id': '889977',
                'author': {'username': 'Jack',
                           'id': '123',
                           'profile_picture_url': 'http://profile.picture.url'},
                'id': '889977'}
        response.json['created_at'] = ''
        self.assertEqual(response.json, wish)

    def test_wish_detail_invalidarg(self):
        response = self.client.get('/wish/889977/', query_string={'invalid':10})
        assert response.status_code == 400

    def test_wish_detail_invalid(self):
        response = self.client.get('/wish/1234/', query_string={})
        assert response.status_code == 404

    def test_wish_detail_mentions(self):
        response = self.client.get('/wish/889977/mentions/', query_string={})
        assert response.status_code == 200
        mentions = {'mentioned_users': [
                        {'id': '1414',
                         'profile_picture_url': 'http://profile.picture.url',
                         'username': 'John'}]}
        self.assertEqual(response.json, mentions)

    def test_wish_detail_hashtags(self):
            response = self.client.get('/wish/93496545/hashtags/', query_string={})
            assert response.status_code == 200
            hashtags = {'hashtags': [
                            {'hashtag': 'old'},
                            {'hashtag': 'birthday'}]}
            self.assertEqual(response.json, hashtags)

    def test_user_list(self):
        response = self.client.get('/user/', query_string={})
        assert response.status_code == 200
        assert len(response.json['users']) == 3

    def test_user_detail(self):
        response = self.client.get('/user/123/', query_string={})
        assert response.status_code == 200
        user = {'username': 'Jack',
                'id': '123',
                'profile_picture_url': 'http://profile.picture.url'}
        self.assertEqual(response.json, user)

    def test_user_detail_invalid(self):
        response = self.client.get('/user/123456/', query_string={})
        assert response.status_code == 404

    def test_user_detail_wishes(self):
        response = self.client.get('/user/63774456/wishes/', query_string={})
        assert response.status_code == 200
        wishes = {'wishes': [
                    {'tweet_text': 'RT @jack: I hope you have a #niceday, @john!',
                     'retweet_tweet_id': '889977',
                     'created_at': '',
                     'id': '889999',
                     'is_retweet': True,
                     'sentiment': 3.0,
                     'author': {'username': 'Charles',
                                'profile_picture_url': 'http://profile.picture.url',
                                'id': '63774456'}}]}

        response.json['wishes'][0]['created_at'] = ''
        self.assertEqual(response.json, wishes)

    def test_user_detail_mentions(self):
        response = self.client.get('/user/1414/mentioned_in/', query_string={})
        assert response.status_code == 200
        wishes = {'wishes': [
                    {'author': {'profile_picture_url': 'http://profile.picture.url',
                                'id': '123',
                                'username': 'Jack'},
                     'created_at': '',
                     'sentiment': 3.0,
                     'is_retweet': False,
                     'tweet_text': 'I hope you have a #niceday, @john!',
                     'id': '889977',
                     'retweet_tweet_id': '889977'},
                    {'author': {'profile_picture_url': 'http://profile.picture.url',
                                'id': '63774456',
                                'username': 'Charles'},
                     'created_at': '',
                     'sentiment': 3.0,
                     'is_retweet': True,
                     'tweet_text': 'RT @jack: I hope you have a #niceday, @john!',
                     'id': '889999',
                     'retweet_tweet_id': '889977'}]}

        response.json['wishes'][0]['created_at'] = ''
        response.json['wishes'][1]['created_at'] = ''
        self.assertEqual(response.json, wishes)

    def test_stats_hashtags(self):
        response = self.client.get('/stats/hashtags/', query_string={})
        assert response.status_code == 200
        hashtags = {'popular_hashtags': [
            {'hashtag': 'niceday', 'count': 2},
            {'hashtag': 'old', 'count': 1},
            {'hashtag': 'birthday', 'count': 1}]}
        self.assertEqual(response.json, hashtags)

    def test_stats_hashtags_count(self):
        response = self.client.get('/stats/hashtags/', query_string={'count': 1})
        assert response.status_code == 200
        hashtags = {'popular_hashtags': [
            {'hashtag': 'niceday', 'count': 2}]}
        self.assertEqual(response.json, hashtags)

    def test_stats_mentions(self):
        response = self.client.get('/stats/mentions/', query_string={})
        assert response.status_code == 200
        mentions = {'popular_users': [
            {'mention_count': 2,
             'user': {'username': 'John',
                      'id': '1414',
                      'profile_picture_url': 'http://profile.picture.url'}}]}
        self.assertEqual(response.json, mentions)

    def test_stats_mentions_count(self):
        response = self.client.get('/stats/mentions/', query_string={'count': 1})
        assert response.status_code == 200
        mentions = {'popular_users': [
            {'mention_count': 2,
             'user': {'username': 'John',
                      'id': '1414',
                      'profile_picture_url': 'http://profile.picture.url'}}]}
        self.assertEqual(response.json, mentions)

    def test_stats_general_interval(self):
        response = self.client.get('/stats/general/', query_string={'from': 0})
        assert response.status_code == 200
        assert len(response.json['stats']) == 4

    def test_stats_general_density(self):
        response = self.client.get('/stats/general/', query_string={'from': 0, 'density': '10m'})
        assert response.status_code == 200
        assert len(response.json['stats']) == 4

    def test_stats_general_empty(self):
        response = self.client.get('/stats/general/', query_string={'density': '10m'})
        assert response.status_code == 200
        assert len(response.json['stats']) == 0


if __name__ == '__main__':
    unittest.main()
