#!/usr/bin/env python3

import os

from flask import Flask, abort
from flask.ext.restless import APIManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.debug = True

# import db models and initialize db
from models import *
db.init_app(app)

manager = APIManager(app, flask_sqlalchemy_db=db)


# Setup CORS to allow javascript clients process the data from API
def add_cors_headers(response):
    # allow accesing this from any source
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

from views import *

# automatic endpoint
manager.create_api(TweetWish, methods=['GET'], results_per_page=-1)

app.after_request(add_cors_headers)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
