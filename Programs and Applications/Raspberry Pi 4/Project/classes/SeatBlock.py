import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from funcs.hx711 import HX711

class SeatBlock:
    def __init__(self, type_str: str):
        self.__type = None
        self.__objects = None
        self.__ready = False
        self.__init_object(type_str)

    def __init_object(self, type_str: str):
        # Analog HX711 Sensor
        if type_str == "HX711":
            self.__type = 0
            self.__init_hx()

        # Optic Fiber Sensor
        elif type_str == "OPTICS":
            self.__type = 1
            self.__init_mcp()
        else:
            raise Exception("Type must be either 'HX711' or 'OPTIC'")

    def __init_hx(self):
        [back_left_dt, back_left_sck] = [8, 7]
        [back_right_dt, back_right_sck] = [6, 13]
        [front_left_dt, front_left_sck] = [23, 24]
        [front_right_dt, front_right_sck] = [27, 22]
        # calibration_unit = -1

        bl_a = 84204.2551
        bl_b = -26.46715
        br_a = 43759.69705
        br_b = -21.07677
        fl_a = 77456.14605
        fl_b = -29.15268
        fr_a = 49617.39939
        fr_b = -33.89369

        hx_bl = HX711(back_left_dt, back_left_sck)
        hx_bl.set_reading_format("MSB", "MSB")
        hx_bl.set_reference_unit(bl_b)
        hx_bl.set_offset(bl_a)

        hx_br = HX711(back_right_dt, back_right_sck)
        hx_br.set_reading_format("MSB", "MSB")
        hx_br.set_reference_unit(br_b)
        hx_br.set_offset(br_a)

        hx_fl = HX711(front_left_dt, front_left_sck)
        hx_fl.set_reading_format("MSB", "MSB")
        hx_fl.set_reference_unit(fl_b)
        hx_fl.set_offset(fl_a)

        hx_fr = HX711(front_right_dt, front_right_sck)
        hx_fr.set_reading_format("MSB", "MSB")
        hx_fr.set_reference_unit(fr_b)
        hx_fr.set_offset(fr_a)

        self.__objects = [hx_bl, hx_br, hx_fl, hx_fr]
        self.__ready = True

    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)
        cs = digitalio.DigitalInOut(board.D16)
        self.__objects = MCP.MCP3008(spi, cs)

    def get_data(self):
        if self.__type == 0 and self.__objects:
            values = []
            for obj in self.__objects():
                values.append(obj.get_weight(5))
                obj.power_down()
                obj.power_up()
            return values
        elif self.__type == 1 and self.__objects:
            pin0 = AnalogIn(self.__objects, MCP.P0)
            pin1 = AnalogIn(self.__objects, MCP.P1)
            pin2 = AnalogIn(self.__objects, MCP.P2)
            pin3 = AnalogIn(self.__objects, MCP.P3)

            return [pin0.value, pin1.value, pin2.value, pin3.value]
        else:
            raise Exception("You need to define the type and initialize the object")
        pass

    def is_ready(self):
        return self.__ready

 """bl_a = 84204.2551
    bl_b = 26.46715
    br_a = 43759.69705
    br_b = 21.07677
    fl_a = 77456.14605
    fl_b = 29.15268
    fr_a = 49617.39939
    fr_b = 33.89369"""
    
    """bl_weight = (bl_mean - bl_a) / bl_b
    br_weight = (br_mean - br_a) / br_b
    fl_weight = (fl_mean - fl_a) / fl_b
    fr_weight = (fr_mean - fr_a) / fr_b"""