from threading import Lock
import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_CONFIG'])
db = SQLAlchemy(app)

from database import Database

db_lock = Lock()
database = Database(db_lock)

from web import views, models


