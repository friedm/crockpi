import sys, threading
from web.crockpi.controller import Controller

from database import Database

if len(sys.argv) != 2:
    print("usage:", sys.argv[0], "<target temp (degrees fahrenheit)>")
    sys.exit(0)

target_temp = int(sys.argv[1])
controller = Controller(database=Database(threading.Lock()))
controller.run(target_temp)

