from web import db
from sqlalchemy.dialects.sqlite import TIMESTAMP

class ControlSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(TIMESTAMP)
    data = db.relationship('Data', backref='session', lazy='dynamic')
    target_temp = db.Column(db.Float)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(TIMESTAMP)
    value = db.Column(db.Float)
    session_id = db.Column(db.Integer, db.ForeignKey('control_session.id'))

class ActiveSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('control_session.id'))


