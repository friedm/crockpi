from web import db, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime

Session = sessionmaker()
Session.configure(bind=create_engine('sqlite:///crockpi.db'))
db_session = Session()

class Database:
    def __init__(self, lock):
        self.__lock = lock

    def store_controller_session(self, timestamp, target_temp):
        control_session = models.ControlSession(time=datetime.utcnow(),target_temp=target_temp)
        db_session.add(control_session)

        self.__lock.acquire()
        db_session.commit()
        self.__lock.release()
    
        return control_session
    
    def store_data(self, session, seconds_since_start, value):
        data = models.Data(session=session,
                seconds_since_start=seconds_since_start,
                value=value)
        db_session.add(data)

        self.__lock.acquire()
        db_session.commit()
        self.__lock.release()

