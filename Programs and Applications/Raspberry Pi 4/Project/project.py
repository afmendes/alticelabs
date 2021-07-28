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

# Initialize cloud
firebase = Firebase()

# Initialize Ergonomics
start_ergonomics(firebase, seat_sensor="OPTIC")

# Initialize Ambient
# start_ambient(firebase, "True")

# Celebrate
# from classes.Ambient import AmbientDHT11
# dht = AmbientDHT11()
# 
# while True:
#     sleep(0.5)
#     dht.is_ready()
#     print("data: " + str(dht.get_data()))
    

