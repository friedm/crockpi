#!/usr/bin/python3

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from web import db
import os.path

db.create_all()

