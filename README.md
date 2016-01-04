# crockpi

Regulate the temperature of a normal crockpot using a raspberry pi, temperature
sensor, and a relay.

## Parts

* Raspberry Pi (any should do)
* DS18B20 1-Wire digital temperature sensor
* Wall-Rated relay (I used a powerswitch tail II, which comes in an enclosure)

## Setup

* Setup the pi for ssh access
* Add `dtoverlay=w1-gpio` to `/boot/config.txt` to enable the onewire kernel module on the pi
* Attach temperature sensor to 5V, ground, and a gpio pin (I used board pin 7)
* Modify your sensor path with the output of `ls /sys/bus/w1/devices`
* Attach relay control pin to board pin 11
* Plug a crockpot or other heating source into the relay
* Place temperature sensor in crockpot
* run `sudo ./src/crockpi <temperature>` to attempt to regulate the sensor
  temperature at `<temperature>`

## Dependencies

* python 3
* wiringpi
* python RPi.GPIO module

## See Also

* [waterproof DS18B20](https://www.sparkfun.com/products/11050)
* [power relay in enclosure](https://www.sparkfun.com/products/10747)
* [using the DS18B20 with the pi](http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi)
* [RPi.GPIO python library](http://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)

## Disclaimer

Recreate this project at your own risk. I am not responsible for any resulting injury or
damage.

