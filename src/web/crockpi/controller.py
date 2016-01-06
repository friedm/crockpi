import time, datetime
from .tempsensor import TempSensor
from .powersupply import PowerSupply

class Controller:
    def __init__(self,values=None,controller_started=None,measurement_taken=None):
        self.__sensor = TempSensor()
        self.__values = values
        self.__start_time = time.time()
        self.__stop = True
        self.__controller_started = controller_started
        self.__measurement_taken = measurement_taken
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
        if self.__controller_started:
            self.__current_session = self.__controller_started(datetime.datetime.utcnow(), target_temp)

        with PowerSupply() as supply:
            self.regulate(target_temp, supply)

    def regulate(self, target_temp, supply):
        while not self.__stop:
            time.sleep(3)

            time_since_start = time.time() - self.__start_time
            actual_temp = self.__sensor.read()
            print("actual temp:", actual_temp)

            self.__values.append((time_since_start, actual_temp))
            if self.__measurement_taken:
                self.__measurement_taken(self.__current_session, time_since_start, actual_temp)
            supply.set(target_temp > actual_temp)

    def stop(self):
        print("stopping controller...")
        self.__stop = True

