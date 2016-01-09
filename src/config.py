import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '2UqSLbnegT9vKvHGjudR'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False

