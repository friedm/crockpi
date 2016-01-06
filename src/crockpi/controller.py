import time, datetime
from powersupply import PowerSupply
from tempsensor import TempSensor
#from web import db, models
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#
#Session = sessionmaker()
#Session.configure(bind=create_engine('sqlite:///../crockpi.db'))
#db_session = Session()

class Controller:
    def __init__(self,values=None,controller_started=None,measurement_taken=None):
        self.__sensor = TempSensor()
        self.__values = values
        self.__start_time = time.time()
        self.__stop = False
        self.__session = None
        self.__controller_started = controller_started
        self.__measurement_taken = measurement_taken

    def run(self, target_temp):
        """
        target_temp: target temperature in fahrenheit

        control the power supply, attempting to keep the
        actual temperature as close to the target temperature
        as possible

        this controller assumes that enabling the power will
        increase the temperature of the sensor
        """

        print("starting temp controller for", target_temp, "degrees fahrenheit")
        if self.__controller_started:
            self.__session = self.__controller_started(datetime.datetime.utcnow(), target_temp)

        with PowerSupply() as supply:
            self.regulate(target_temp, supply)

#    def write_session(self):
#        self.__session = models.ControlSession(time=datetime.datetime.utcnow())
#        db_session.add(self.__session)
#        db_session.commit()

    def regulate(self, target_temp, supply):
        while not self.__stop:
            time.sleep(3)

            time_since_start = time.time() - self.__start_time
            actual_temp = self.__sensor.read()
            print("actual temp:", actual_temp)

            if self.__measurement_taken:
                self.__measurement_taken(self.__session, time_since_start, measurement_taken)
#            supply.set(target_temp > actual_temp)
#            data = models.Data(session=self.__session,
#                    seconds_since_start=time_since_start,
#                    value=self.__sensor.read())
#
#            db_session.add(data)
#            db_session.commit()

    def stop(self):
        print("stopping controller...")
        self.__stop = True








