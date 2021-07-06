import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

from funcs.hx711 import HX711


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
        self.__ready = True

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
        elif type_str == "OPTIC":
            self.__type = 1
            self.__init_mcp()
        else:
            raise Exception("Type must be either 'HX711' or 'OPTIC'")

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

    def __init_mcp(self):
        spi = busio.SPI(clock=board.SCK_1, MISO=board.MISO_1, MOSI=board.MOSI_1)
        cs = digitalio.DigitalInOut(board.D16)
        self.__objects = MCP.MCP3008(spi, cs)

    def get_data(self):
        if self.__type == 0 and self.__objects:
            values = []
            values_raw = []

            count = 0
            for obj in self.__objects:
                count += 1
                x = obj.get_weight()
                if count == 1:
                    values_raw.append(x)
                    values.append(
                        41.8693702120154 - 1.23799318169326e-13 * (
                                    (1.37628314068967e23 * x + 8.62319892347033e29) ** (1 / 2))
                    )
                if count == 2:
                    values_raw.append(x)
                    values.append(
                        96.8860931513110 - 2.92883195708374e-13 * (
                                    (7.85815085221659e22 * x + 9.86736172185844e28) ** (1 / 2))
                    )
                if count == 3:
                    values_raw.append(x)
                    values.append(
                        109.028756919783 - 2.00984001217932e-11 * (
                                    (1.22288230549622e19 * x - 9.50698869729724e24) ** (1 / 2))
                    )
                if count == 4:
                    values_raw.append(x)
                    values.append(
                        53.9002485907030 - 5.32256772313580e-13 * (
                                    (7.39208825591957e21 * x - 8.19710069793331e27) ** (1 / 2))
                    )
                obj.reset()

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

