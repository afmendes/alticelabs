from time import sleep, time
from datetime import datetime

from classes.File import File
from classes.Cloud import Cloud
from classes.Ambient import *
from classes.Firebase import Firebase


def start_ambient(cloud: Cloud):

    # Initialize DHT11 Sensor
    dht = _dht11_initialize()

    # Initialize MCP3008 ADC
    mcp = _mcp3008_initialize()

    # Initialize Accelerometer Sensor
    accel = _accelerometer_initialize()

    # Initialize coprocessor
    _coprocessor(cloud, dht, mcp, accel)


# -------------------- DHT11 --------------------
def _dht11_initialize():
    return AmbientDHT11()


def _dth11_get_data(dht: AmbientDHT11):
    return dht.get_data()


# ------------------- MCP3008 -------------------
def _mcp3008_initialize():
    return AmbientMCP3008()


def _mcp3008_get_data(mcp: AmbientMCP3008):
    return mcp.get_data()


# ---------------- Accelerometer ----------------
def _accelerometer_initialize():
    return AmbientAccelerometer()


def _accelerometer_get_data(accel: AmbientAccelerometer):
    return accel.get_data()


# ------------------ Coprocessor ----------------
def _coprocessor(cloud: Cloud, dht: AmbientDHT11, mcp: AmbientMCP3008, accel: AmbientAccelerometer):

    while not dht.is_ready() and not mcp.is_ready() and not accel.is_ready():
        sleep(0.5)

    try:
        while True:
            start_time = time()

            dht_data = _dth11_get_data(dht)
            mcp_data = _mcp3008_get_data(mcp)
            accel_data = _accelerometer_get_data(accel)

            while (time() - start_time) < 5:
                sleep(0.1)

            _send_data(cloud, dht_data, mcp_data, accel_data)

    except Exception as e:
        print(e)
        start_ambient(cloud)

def _send_data(cloud: Firebase, dht_data, mcp_data, accel_data):
    flag_cloud = True
    flag_file = False
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if flag_cloud:
        # DHT
        temperature = dht_data[0]
        humidity = dht_data[2]

        cloud.push_dht_data(temperature, humidity, date)
        pass

    if flag_file:
        file = File("output/Ambient/test.csv")
        file.write("""
        DHT11: {}
        MCP3008: {}
        Accelerometer: {}""".format(dht_data, mcp_data, accel_data))




































    pass

