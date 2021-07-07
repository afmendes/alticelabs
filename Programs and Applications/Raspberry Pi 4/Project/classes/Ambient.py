import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_dht import DHT11
from time import sleep


class AmbientMCP3008:
    def __init__(self):
        self.__object = False
        self.__ready = False
        self.__init_mcp()

    def is_ready(self):
        return self.__ready

    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)
        cs = digitalio.DigitalInOut(board.D16)
        self.__object = MCP.MCP3008(spi, cs)
        self.__ready = True

    def get_data(self):

        def get_luminosity():
            pin4 = AnalogIn(self.__object, MCP.P4)
            luminosity = pin4.value
            return luminosity

        def get_noise():
            pin5 = AnalogIn(self.__object, MCP.P5)
            noise = pin5.value
            return noise

        def get_co2():
            def get_samples():
                pin6 = AnalogIn(self.__object, MCP.P6)

                number_of_samples = 50
                sample_interval = 0.005

                volts_sum = 0
                for i in range(number_of_samples):
                    volts_sum += pin6.voltage
                    sleep(sample_interval)

                return volts_sum/number_of_samples

            def MGGetPercentage():

                zero_point_voltage = 0.17
                DC_gain = 8.5

                reaction_voltage = 0.030  # adjustable value

                CO2_curve = [2.602, zero_point_voltage, round((reaction_voltage / (2.602 - 3)), 2)]

                if (volts / DC_gain) >= zero_point_voltage:
                    return -1
                else:
                    return pow(10, ((volts / DC_gain) - CO2_curve[1]) / CO2_curve[2] + CO2_curve[0])

            volts = get_samples()

            return str(MGGetPercentage()*100) + "%"

        def get_body_temperature():
            pin7 = AnalogIn(self.__object, MCP.P7)
            return round(pin7.voltage * 100, 1)  # Value in ºC -- 10 mV / ºC -- 0V @ 0ºC

        return get_luminosity(), get_noise(), get_co2(), get_body_temperature()


class AmbientDHT11:
    def __init__(self):
        self.__ready = False
        self.device = DHT11(board.D17)
        self.__ready = True

    def is_ready(self):
        return self.__ready

    def get_data(self):
        temp_c = self.device.temperature
        temp_f = temp_c * (9 / 5) + 32
        hum = self.device.humidity
        return round(temp_c, 1), round(temp_f, 1), round(hum)

