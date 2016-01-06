#!/usr/bin/python3

import sys
from controller import Controller

if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<target temp (degrees fahrenheit)>")
    sys.exit(0)

target_temp = int(sys.argv[1])
controller = Controller()
controller.run(target_temp)

