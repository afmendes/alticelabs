import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class BackBlock:
    def __init__(self):
        self.__ready = False
        self.__object = False
        self.__init_mcp()

    def is_ready(self):
        return self.__ready

    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        self.__object = MCP.MCP3008(spi, cs)

    def get_data(self):
        pin0 = AnalogIn(self.__object, MCP.P0)
        pin1 = AnalogIn(self.__object, MCP.P1)
        pin2 = AnalogIn(self.__object, MCP.P2)
        pin3 = AnalogIn(self.__object, MCP.P3)
        pin4 = AnalogIn(self.__object, MCP.P4)
        pin5 = AnalogIn(self.__object, MCP.P5)
        pin6 = AnalogIn(self.__object, MCP.P6)
        pin7 = AnalogIn(self.__object, MCP.P7)

        return (pin0.value, pin1.value, pin2.value, pin3.value,
                pin4.value, pin5.value, pin6.value, pin7.value)
