import math
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from funcs.hx711 import HX711


# backrest class
class BackBlock:
    # class initializer
    def __init__(self):
        self.__ready = False
        self.__object = False
        self.__init_mcp()

    # return ready state of the mcp3008
    def is_ready(self):
        return self.__ready

    # initialize MCP3008 on 1st SPI
    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        cs = digitalio.DigitalInOut(board.D5)
        self.__object = MCP.MCP3008(spi, cs)
        self.__ready = True

    # function to retrieve data from the MCP3008 (FSR sensors)
    def get_data(self):
        # pins 1,3,5 and 7 are unused
        pin0 = AnalogIn(self.__object, MCP.P0)
        pin2 = AnalogIn(self.__object, MCP.P2)
        pin4 = AnalogIn(self.__object, MCP.P4)
        pin6 = AnalogIn(self.__object, MCP.P6)

        return pin0.value, pin2.value, pin4.value, pin6.value


# seat class
class SeatBlock:
    # class initializer
    def __init__(self, type_str: str):
        self.__type = None
        self.__objects = None
        self.__ready = False
        self.__init_object(type_str)

    # initialize seat sensors with choice between hx711 and optics
    def __init_object(self, type_str: str):
        # Analog HX711 Sensor
        if type_str == "HX711":
            self.__type = 0
            self.__init_hx()

        # Optic Fiber Sensor
        elif type_str == "OPTIC":
            self.__type = 1
            self.__init_mcp()
        else:
            raise Exception("Type must be either 'HX711' or 'OPTIC'")

    # initialize HX711 sensors
    def __init_hx(self):
        [back_left_dt, back_left_sck] = [8, 7]
        [back_right_dt, back_right_sck] = [23, 24]
        [front_left_dt, front_left_sck] = [6, 13]
        [front_right_dt, front_right_sck] = [27, 22]
        
        hx_bl = HX711(back_left_dt, back_left_sck)
        hx_bl.set_reading_format("MSB", "MSB")
        hx_bl.set_reference_unit(1)
        hx_bl.set_offset_B(0)

        hx_br = HX711(back_right_dt, back_right_sck)
        hx_br.set_reading_format("MSB", "MSB")
        hx_br.set_reference_unit(1)
        hx_br.set_offset_B(0)

        hx_fl = HX711(front_left_dt, front_left_sck)
        hx_fl.set_reading_format("MSB", "MSB")
        hx_fl.set_reference_unit(1)
        hx_fl.set_offset_B(0)

        hx_fr = HX711(front_right_dt, front_right_sck)
        hx_fr.set_reading_format("MSB", "MSB")
        hx_fr.set_reference_unit(1)
        hx_fr.set_offset_B(0)

        self.__objects = [hx_bl, hx_br, hx_fl, hx_fr]
        self.__ready = True

    # Initialize 2nd MCP3008
    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)
        cs = digitalio.DigitalInOut(board.D16)
        self.__objects = MCP.MCP3008(spi, cs)

    # Retrieves data from seat sensors
    def get_data(self):
        # HX711 sensors
        if self.__type == 0 and self.__objects:
            values = []
            values_raw = []

            count = 0
            # Back right - Back Left - Front Right - Front Left
            # This loop calculates the equivalent of weight using the digital output of MCP3008
            for obj in self.__objects:
                count += 1
                x = obj.get_weight()
                # Back right
                if count == 1:
                    values_raw.append(x)
                    values.append(
                        abs(24.7186-0.0000310184*(1.61195e6*x-2.77615e12)**(0.5))
                    )
                # Back Left
                if count == 2:
                    values_raw.append(x)
                    values.append(
                         abs(29.1023-0.0000366446*(1.36446e6*x-1.25333e12)**(0.5))  
                    )
                # Front Right
                if count == 3:
                    values_raw.append(x)
                    values.append(
                        abs(117.013-0.000103555*(482833*x+3.30304e12)**(0.5))
                    )
                # Front Left
                if count == 4:
                    values_raw.append(x)
                    values.append(
                        abs(134.211-0.000125223*(399287*x+4.11594e10)**(0.5))
                    )
                obj.reset()

            return values_raw
        # Optics sensors
        elif self.__type == 1 and self.__objects:
            pin0 = AnalogIn(self.__objects, MCP.P0)  # Front Right
            pin1 = AnalogIn(self.__objects, MCP.P1)  # Back Left
            pin2 = AnalogIn(self.__objects, MCP.P2)  # Back Right
            pin3 = AnalogIn(self.__objects, MCP.P3)  # Front Left

            # Back right - Back Left - Front Right - Front Left
            return [pin2.voltage, pin1.voltage, pin0.voltage, pin3.voltage]
        else:
            raise Exception("You need to define the type and initialize the object")
        pass

    # returns ready state of the class
    def is_ready(self):
        return self.__ready

