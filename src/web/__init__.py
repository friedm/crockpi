from threading import Lock

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from database import Database

db_lock = Lock()
database = Database(db_lock)

from web import views, models


