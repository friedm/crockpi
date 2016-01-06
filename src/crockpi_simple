#!/usr/bin/python3

"""
Control at a certain temperature, without recording any data.
"""

import sys
from web.crockpi.controller import Controller

if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<target temp (degrees fahrenheit)>")
    sys.exit(0)

target_temp = int(sys.argv[1])
controller = Controller()
controller.run(target_temp)

