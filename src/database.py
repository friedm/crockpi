from web import db, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

Session = sessionmaker()
Session.configure(bind=create_engine('sqlite:///crockpi.db'))
db_session = Session()

def store_controller_session(timestamp, target_temp):
    control_session = models.ControlSession(time=datetime.utcnow(),target_temp=target_temp)
    db_session.add(control_session)
    db_session.commit()

    return control_session

def store_data(session, seconds_since_start, value):
    data = models.Data(session=session,
            seconds_since_start=seconds_since_start,
            value=value)
    db_session.add(data)
    db_session.commit()

