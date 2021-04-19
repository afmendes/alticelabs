from datetime import datetime
import time
import json

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from threading import Thread

from classes.Queue import Queue
from classes.Cloud import Cloud
from classes.File import File

mcp0_queue = Queue()
mcp1_queue = Queue()


#TODO: Separate data sent to the cloud based on pins
def start_mcp(cloud: Cloud, flag_debug=False, flag_print=False,
              flag_file=False, flag_cloud=True):
    if flag_debug:
        print("Initializing MCPs")
    mcp0, mcp1 = init_mcps()

    if flag_debug:
        print("Initializing threads")
    mcp0_thread = Thread(target=read_mcp, args=(mcp0, mcp0_queue))
    mcp1_thread = Thread(target=read_mcp, args=(mcp1, mcp1_queue))

    if flag_debug:
        print("Starting threads")
    mcp0_thread.start()
    mcp1_thread.start()

    """
    file = None
    if flag_file:
        file = File(filename, filepath)
    """

    while True:
        # MP0: Used for back FSR sensors for back positions
        if not mcp0_queue.is_empty():
            if flag_debug:
                print("Getting MCP0 data")
            data = mcp0_queue.dequeue()
            if flag_cloud:
                if flag_debug:
                    print("Sending MCP0 data to cloud")
                # TODO: CLOUD and files
                pins_data = data[0]
                time = data[1]
                # Separate data by pins
                pin0_data = pins_data[0]
                pin1_data = pins_data[1]
                pin2_data = pins_data[2]
                pin3_data = pins_data[3]
                pin4_data = pins_data[4]
                pin5_data = pins_data[5]
                pin6_data = pins_data[6]
                pin7_data = pins_data[7]
                # Distinguish pin data and process it by location
                # TODO: Know what position corresponds each data
                # TODO: Decide whether to use max, mean or something else
                some_position_a = max(pin0_data, pin1_data)
                some_position_b = max(pin2_data, pin3_data)
                some_position_c = max(pin4_data, pin5_data)
                some_position_d = max(pin6_data, pin7_data)
                if flag_print:
                    "Do something"
                    print("Some Position A:", some_position_a)
                    print("Some Position B:", some_position_b)
                    print("Some Position C:", some_position_c)
                    print("Some Position D:", some_position_d)
                if flag_file:
                    "Do something"
                    file = File("back.csv", "output/MCP3008")
                    file.write((some_position_a, some_position_b, some_position_c, some_position_d),
                               headers="Some Position A,Some Position B,Some Position C,Some Position D")
                if flag_cloud:
                    "Do something"
                    # cloud.post_data(stream_name="MCP0", data_json=data[0], timestamp=data[1])

            if flag_print:
                print("MCP0:")
                print(data[0])
            if flag_file:
                'file.write(data="MCP0: " + str(data))'

        # MP1: Used for seat optic sensors and some ambient sensors
        if not mcp1_queue.is_empty():
            if flag_debug:
                print("Getting MCP1 data")
            data = mcp1_queue.dequeue()
            if flag_cloud:
                if flag_debug:
                    print("Sending MCP1 data to cloud")
                # TODO: CLOUD and files
                # TODO: Know what position and sensor corresponds each data
                pins_data = data[0]
                time = data[1]
                sensor_a = pins_data[0]
                sensor_b = pins_data[1]
                sensor_c = pins_data[2]
                sensor_d = pins_data[3]
                some_position_a = pins_data[4]
                some_position_b = pins_data[5]
                some_position_c = pins_data[6]
                some_position_d = pins_data[7]
                #cloud.post_data(stream_name="MCP1", data_json=data[0], timestamp=data[1])
            if flag_print:
                print("MCP1:")
                print(data[0])
            if flag_file:
                'file.write(data="MCP1: " + str(data))'


def init_mcps():
    # create the spi bus
    spi0 = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    spi1 = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)

    # create the cs (chip select)
    cs0 = digitalio.DigitalInOut(board.D5)
    cs1 = digitalio.DigitalInOut(board.D16)

    # create the mcp object
    mcp0 = MCP.MCP3008(spi0, cs0)
    mcp1 = MCP.MCP3008(spi1, cs1)

    return mcp0, mcp1


def read_mcp(mcp, queue: Queue):
    while True:
        pin0 = AnalogIn(mcp, MCP.P0)
        pin1 = AnalogIn(mcp, MCP.P1)
        pin2 = AnalogIn(mcp, MCP.P2)
        pin3 = AnalogIn(mcp, MCP.P3)
        pin4 = AnalogIn(mcp, MCP.P4)
        pin5 = AnalogIn(mcp, MCP.P5)
        pin6 = AnalogIn(mcp, MCP.P6)
        pin7 = AnalogIn(mcp, MCP.P7)
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        data = {
            "pin0": pin0.value,
            "pin1": pin1.value,
            "pin2": pin2.value,
            "pin3": pin3.value,
            "pin4": pin4.value,
            "pin5": pin5.value,
            "pin6": pin6.value,
            "pin7": pin7.value
        }
        queue.enqueue((data, date))
        time.sleep(0.5)


def test():
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 0
    chan = AnalogIn(mcp, MCP.P0)

    while True:
        print('Raw ADC Value: ', chan.value)
        print('ADC Voltage: ' + str(chan.voltage) + 'V')
        time.sleep(1)
