import board
import time

from adafruit_dht import DHT11
from datetime import datetime

from classes.File import File


def start_dht(flag_debug, flag_print, flag_file, flag_cloud, filename, filepath):
    dht = init_dht(flag_debug)
    if flag_file:
        file = File(filename, filepath)

    while True:
        try:
            if flag_debug:
                print("[DEBUG] Getting DHT data.")
            temperature = dht.temperature
            humidity = dht.humidity

            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if flag_print:
                print("[DATA DHT] Temperature: {}\nHumidity: {}%".format(temperature, humidity))

            if flag_file:
                file.write((temperature, humidity))



            time.sleep(5)
        except Exception as error:
            dht.exit()
            raise error


def init_dht(flag_debug):
    if flag_debug:
        print("[DEBUG] Getting DHT11 at GPIO 17.")
    dhtDevice = DHT11(board.D17)
    if flag_debug:
        print("[DEBUG] DHT11 connected.")
    return dhtDevice


def test():
    # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
    # SPDX-License-Identifier: MIT

    import time

    # Initial the dht device, with data pin connected to:
    dhtDevice = DHT11(board.D17)

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)
