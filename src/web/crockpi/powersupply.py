import RPi.GPIO as GPIO

class PowerSupply:
    __pin = 11 # board pin 11, wiringpi pin 0

    def set(self, value):
        if value:
            self.__write(1)
        else:
            self.__write(0)

    def __write(self, value):
        GPIO.output(PowerSupply.__pin,value)

    def __enter__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(PowerSupply.__pin, GPIO.OUT)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.set(False)

