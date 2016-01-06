#!/usr/bin/python3

import sys
from web.crockpi.controller import Controller

from database import store_controller_session, store_data

if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<target temp (degrees fahrenheit)>")
    sys.exit(0)

target_temp = int(sys.argv[1])
controller = Controller(controller_started=store_controller_session,measurement_taken=store_data)
controller.run(target_temp)

