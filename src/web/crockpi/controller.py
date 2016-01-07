import time, datetime
from .tempsensor import TempSensor
from .powersupply import PowerSupply

class Controller:
    def __init__(self,values=None,database=None):
        self.__sensor = TempSensor()
        self.__values = values
        self.__stop = True
        self.__database = database
        self.__current_session = None

    def run(self, target_temp):
        """
        target_temp: target temperature in fahrenheit

        control the power supply, attempting to keep the
        actual temperature as close to the target temperature
        as possible

        this controller assumes that enabling the power will
        increase the temperature of the sensor
        """

        self.__stop = False

        print("starting temp controller for", target_temp, "degrees fahrenheit")
        with PowerSupply() as supply:
            self.regulate(target_temp, supply)

    def regulate(self, target_temp, supply):
        while not self.__stop:
            timestamp = datetime.datetime.now()
            actual_temp = self.__sensor.read()
            print("actual temp:", actual_temp)

            self.__values.append((timestamp, actual_temp))

            if self.__database:
                self.__database.store_data(timestamp, actual_temp)
            supply.set(target_temp > actual_temp)

            time.sleep(3)


    def stop(self):
        print("stopping controller...")
        self.__stop = True

