# crockpi

## Parts

* Raspberry Pi (I used a Zero)
* DS18B20 1-Wire digital temperature sensor
  (I used https://www.sparkfun.com/products/11050)
* Wall-Rated relay (I used this enclosed relay https://www.sparkfun.com/products/10747)

## Setup

Add `dtoverlay=w1-gpio` to `/boot/config.txt` to enable the onewire kernel module on the pi.
