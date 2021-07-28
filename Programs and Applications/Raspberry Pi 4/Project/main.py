from threading import Thread
from subprocess import check_output
import os
import signal
from time import sleep

from classes.Firebase import Firebase

from funcs.ergonomics import start_ergonomics
from funcs.ambient import start_ambient
from funcs.heartbeat import start_heartbeat
from funcs.respiration import start_respiration
    
def get_pid(name):
    return check_output(["pidof",name])

try:
    os.kill(int(get_pid("libgpiod_pulsein")),signal.SIGTERM)
    print("libgpiod_pulsein process killed")
    print("Waiting 3 seconds..")
    sleep(3)
    print("Program is starting..")
except:
    ...


firebase = Firebase()

# "HX711" or "OPTIC"
seat_sensor = "OPTIC"

if seat_sensor == "HX711":
    # Initialize Ergonomics
    thread_ergonomics = Thread(target=start_ergonomics, args=(firebase,"OPTIC",))
    thread_ergonomics.start()
    
    # Initialize Ambient
    thread_ambient = Thread(target=start_ambient, args=(firebase,))
    thread_ambient.start()
else:
    # Initialize Ambient
    thread_ambient = Thread(target=start_ambient, args=(firebase, "True", ))
    thread_ambient.start()

# Initialize Heartbeat
# thread_heartbeat = Thread(target=start_heartbeat, args=(firebase,))
# thread_heartbeat.start()

# Initialize Respiration
thread_respiration = Thread(target=start_respiration, args=(firebase,))
thread_respiration.start()

# Celebrate
" (ɔ◔‿◔)ɔ ♥ "
