from web import db, models
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import scoped_session,sessionmaker

from datetime import datetime

class Database:
    def __init__(self, lock):
        self.__lock = lock
        session_factory = sessionmaker(bind=create_engine('sqlite:///crockpi.db'))
        self.__session_creator = scoped_session(session_factory)

    def store_controller_session(self, timestamp, target_temp):
        control_session = models.ControlSession(time=datetime.utcnow(),target_temp=target_temp)

        db.session.add(control_session)
        self.__lock.acquire()
        db.session.commit()
        self.__lock.release()

        print('storing session', control_session.id)

        return control_session.id
    
    def store_data(self, time, value):
        session = self.get_active_session()

        if not session:
            print('no active session! cannot store data!')
            return

        data = models.Data(session=session,
                time=time,
                value=value)

        db.session.add(data)

        self.__lock.acquire()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            print('failed to store data');
        self.__lock.release()

    def retrieve_data(self, session):
        self.__lock.acquire()
        all_data_values = db.session.query(models.Data).filter(models.Data.session_id==session.id).all()
        self.__lock.release()

        return list(map(lambda data: [data.time, data.value], all_data_values))

    def add_active_session(self, session_id):
        print('adding active session with id', session_id)
        active_session = models.ActiveSession(session_id=session_id)
        db.session.add(active_session)

        self.__lock.acquire()
        db.session.commit()
        self.__lock.release()

    def get_active_session(self):
        self.__lock.acquire()
        active_session = db.session.query(models.ActiveSession).all()
        self.__lock.release()

        if len(active_session) != 1:
            return None

        active_id = active_session[0].session_id

        self.__lock.acquire()
        session = db.session.query(models.ControlSession).filter(models.ControlSession.id==active_id).one()
        self.__lock.release()
        return session

    def delete_active_session(self):
        db.session.query(models.ActiveSession).delete()

        self.__lock.acquire()
        db.session.commit()
        self.__lock.release()

    def get_latest_sessions(self):
        current_session = self.get_active_session()
        current_id = -1
        if current_session: current_id = current_session.id

        self.__lock.acquire()
        sessions = db.session.query(models.ControlSession).filter(models.ControlSession.id!=current_id).order_by(desc(models.ControlSession.time)).limit(5).all()
        self.__lock.release()
        return sessions

