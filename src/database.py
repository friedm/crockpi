from web import db, models
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from datetime import datetime

class Database:
    def __init__(self, lock):
        self.__lock = lock
        session_factory = sessionmaker(bind=create_engine('sqlite:///crockpi.db'))
        self.__session_creator = scoped_session(session_factory)

    def store_controller_session(self, timestamp, target_temp):
        control_session = models.ControlSession(time=datetime.utcnow(),target_temp=target_temp)

        self.__lock.acquire()
        db_session = self.__session_creator()
        db_session.add(control_session)
        db_session.commit()

        print('storing session', control_session.id)

        self.__session_creator.remove()
        self.__lock.release()
    
        return control_session.id
    
    def store_data(self, time, value):
        session = self.get_active_session()

        if not session:
            print('no active session! cannot store data!')
            return

        data = models.Data(session=session,
                time=time,
                value=value)

        db_session = self.__session_creator()
        db_session.add(data)

        self.__lock.acquire()
        db_session.commit()
        self.__lock.release()
        self.__session_creator.remove()

    def retrieve_data(self, session):
        db_session = self.__session_creator()

        self.__lock.acquire()
        all_data_values = db_session.query(models.Data).filter(models.Data.session_id==session.id).all()
        self.__lock.release()

        return list(map(lambda data: [data.time, data.value], all_data_values))

    def add_active_session(self, session_id):
        self.__lock.acquire()
        db_session = self.__session_creator()
        print('adding active session with id', session_id)
        active_session = models.ActiveSession(session_id=session_id)

        db_session.add(active_session)
        db_session.commit()
        self.__session_creator.remove()
        self.__lock.release()

    def get_active_session(self):
        self.__lock.acquire()
        db_session = self.__session_creator()
        active_session = models.ActiveSession.query.all()
        self.__session_creator.remove()
        self.__lock.release()

        if len(active_session) != 1:
            return None

        active_id = active_session[0].session_id

        self.__lock.acquire()
        db_session = self.__session_creator()
        session = db_session.query(models.ControlSession).filter(models.ControlSession.id==active_id).one()
        self.__session_creator.remove()
        self.__lock.release()
        return session

    def delete_active_session(self):
        self.__lock.acquire()
        db_session = self.__session_creator()
        db_session.query(models.ActiveSession).delete()
        db_session.commit()
        self.__session_creator.remove()
        self.__lock.release()

