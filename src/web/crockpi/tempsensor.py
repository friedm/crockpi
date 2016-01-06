
class TempSensor:
    __sensor_path = '/sys/bus/w1/devices/28-00000652b8e4/w1_slave'

    def __init__(self):
        self.__recent_values = []

    def read(self):
        data = self.__read_sensor_file()
        temp_value = self.__parse_sensor_data(data)
        fahrenheit_value = self.__convert_to_fahrenheit(temp_value)
        self.__recent_values.append(fahrenheit_value)
        while len(self.__recent_values) > 5:
            self.__recent_values.pop(0)
        return sum(self.__recent_values) / float(len(self.__recent_values))

    def __read_sensor_file(self):
        f = open(TempSensor.__sensor_path,'r')
        contents = f.read()
        f.close()
        return contents

    def __parse_sensor_data(self, data):
        return int(data.split('t=')[-1])/1000

    def __convert_to_fahrenheit(self, celsius):
        return (celsius * 1.8) + 32



