from time import sleep, time
from datetime import datetime

from classes.File import File
from classes.Ambient import *
from classes.Firebase import Firebase


def start_ambient():

    firebase = Firebase()

    # Initialize DHT11 Sensor
    dht = _dht11_initialize()

    # Initialize MCP3008 ADC
    mcp = _mcp3008_initialize()

    # Initialize coprocessor
    _coprocessor(firebase, dht, mcp)


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


# ------------------ Coprocessor ----------------
def _coprocessor(firebase: Firebase, dht: AmbientDHT11, mcp: AmbientMCP3008):

    while not dht.is_ready() and not mcp.is_ready():
        sleep(0.5)

    try:
        while True:
            start_time = time()

            dht_data = _dth11_get_data(dht)
            mcp_data = _mcp3008_get_data(mcp)

            while (time() - start_time) < 5:
                sleep(0.1)

            _send_data(firebase, dht_data, mcp_data)

    except Exception as e:
        print(e)
        start_ambient()


def _send_data(firebase: Firebase, dht_data, mcp_data):
    flag_cloud = True
    flag_file = False
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if flag_cloud:

        # DHT11
        temperature = dht_data[0]
        humidity = dht_data[2]
        firebase.push_dht_data(temperature, humidity, date)

        # MCP1
        luminosity, noise, co2_read, body_temperature = mcp_data
        firebase.push_mcp_data(luminosity, co2_read, noise, date)
        firebase.push_ergonomics_body_temperature(body_temperature, date)

    if flag_file:
        file = File("output/Ambient/test.csv")
        file.write("""
        DHT11: {}
        MCP3008: {}""".format(dht_data, mcp_data))




































    pass

