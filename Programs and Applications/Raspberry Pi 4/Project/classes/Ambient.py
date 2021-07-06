import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_dht import DHT11


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
        pin4 = AnalogIn(self.__object, MCP.P4)
        pin5 = AnalogIn(self.__object, MCP.P5)
        pin6 = AnalogIn(self.__object, MCP.P6)
        pin7 = AnalogIn(self.__object, MCP.P7)

        return pin4.value, pin5.value, pin6.value, pin7.value


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
        return temp_c, temp_f, hum

