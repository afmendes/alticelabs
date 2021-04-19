import time
import sys
from datetime import datetime
import numpy

import RPi.GPIO as GPIO
from threading import Thread

from .hx711 import HX711
from classes.Queue import Queue
from classes.File import File
from classes.Cloud import Cloud


def clean_exit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def start_seat(cloud: Cloud, flag_debug, flag_print, flag_file, flag_cloud, filename, filepath):

    # Variables
    max_samples = 50

    back_left_dt = 8
    back_left_sck = 7
    back_right_dt = 6
    back_right_sck = 13
    front_left_dt = 23
    front_left_sck = 24
    front_right_dt = 27
    front_right_sck = 22
    calibration_unit = -1

    bl_a = 84204.2551
    bl_b = 26.46715
    br_a = 43759.69705
    br_b = 21.07677
    fl_a = 77456.14605
    fl_b = 29.15268
    fr_a = 49617.39939
    fr_b = 33.89369

    bl_queue = Queue()
    br_queue = Queue()
    fl_queue = Queue()
    fr_queue = Queue()

    bl_arr = []
    br_arr = []
    fl_arr = []
    fr_arr = []

    try:
        # Initializing threads
        bl_t = Thread(target=read_load, args=(back_left_dt,  back_left_sck,
                                              calibration_unit, bl_queue))
        br_t = Thread(target=read_load, args=(back_right_dt, back_right_sck,
                                              calibration_unit, br_queue))
        fl_t = Thread(target=read_load, args=(front_left_dt, front_left_sck,
                                              calibration_unit, fl_queue))
        fr_t = Thread(target=read_load, args=(front_right_dt, front_right_sck,
                                              calibration_unit, fr_queue))
        # Starting threads
        bl_t.start()
        br_t.start()
        fl_t.start()
        fr_t.start()

        while True:
            if not bl_queue.is_empty():
                bl_arr.append(bl_queue.dequeue())

            if not br_queue.is_empty():
                br_arr.append(br_queue.dequeue())

            if not fl_queue.is_empty():
                fl_arr.append(fl_queue.dequeue())

            if not fr_queue.is_empty():
                fr_arr.append(fr_queue.dequeue())
        
            if len(bl_arr) >= max_samples or len(br_arr) >= max_samples \
                    or len(br_arr) >= max_samples or len(br_arr) >= max_samples:

                bl_mean = numpy.mean([x[0] for x in bl_arr])
                br_mean = numpy.mean([x[0] for x in br_arr])
                fl_mean = numpy.mean([x[0] for x in fl_arr])
                fr_mean = numpy.mean([x[0] for x in fr_arr])

                bl_weight = (bl_mean - bl_a) / bl_b
                br_weight = (br_mean - br_a) / br_b
                fl_weight = (fl_mean - fl_a) / fl_b
                fr_weight = (fr_mean - fr_a) / fr_b

                print("BL:", bl_weight, "\n",
                      "BR:", br_weight, "\n",
                      "FL:", fl_weight, "\n",
                      "FR:", fr_weight)

                bl_arr = []
                br_arr = []
                fl_arr = []
                fr_arr = []

    except (KeyboardInterrupt, SystemExit):
        clean_exit()
    pass


def read_load(DT, SCK, referenceUnit, queue):
    hx = HX711(DT, SCK)
    init_load(hx, referenceUnit)
    while True:

        val = hx.get_weight(5)
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        queue.enqueue((val, date))

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)


def init_load(hx, referenceUnit):
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(referenceUnit)
    hx.reset()
    hx.tare()
