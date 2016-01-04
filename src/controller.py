import time
from powersupply import PowerSupply
from tempsensor import TempSensor

class Controller:
    def __init__(self,values=None):
        self.__sensor = TempSensor()
        self.__values = values
        self.__start_time = time.time()
        self.__stop = False

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
        with PowerSupply() as supply:
            self.regulate(target_temp, supply)


    def regulate(self, target_temp, supply):
        while not self.__stop:
            time.sleep(3)

            actual_temp = self.__sensor.read()
            print("actual temp:", actual_temp)

            supply.set(target_temp > actual_temp)
            self.__values.append((time.time() - self.__start_time,
                self.__sensor.read()))


    def stop(self):
        print("stopping controller...")
        self.__stop = True








