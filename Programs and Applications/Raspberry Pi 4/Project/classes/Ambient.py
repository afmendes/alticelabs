import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import smbus
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


class AmbientAccelerometer:
    def __init__(self):
        self.bus = None
        self.__ready = False
        self.__init_dht11()

    def is_ready(self):
        return self.__ready

    def __init_dht11(self):

        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x00(00)  StandBy mode
        self.bus.write_byte_data(0x1D, 0x2A, 0x00)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x01(01)  Active mode
        self.bus.write_byte_data(0x1D, 0x2A, 0x01)

        # MMA8452Q address, 0x1C(28)
        # Select Configuration register, 0x0E(14)
        # 0x00(00)  Set range to +/- 2g
        self.bus.write_byte_data(0x1D, 0x0E, 0x00)

        self.__ready = True

    def get_data(self):
        try:
            # MMA8452Q address, 0x1d(28)
            # Read data back from 0x00(0), 7 bytes
            # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
            data = self.bus.read_i2c_block_data(0x1D, 0x00, 7)

            # Convert the data
            x_accel = (data[1] * 256 + data[2]) / 16
            if x_accel > 2047:
                x_accel -= 4095

            y_accel = (data[3] * 256 + data[4]) / 16
            if y_accel > 2047:
                y_accel -= 4095

            z_accel = (data[5] * 256 + data[6]) / 16
            if z_accel > 2047:
                z_accel -= 4095

            return x_accel, y_accel, z_accel

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])

        except Exception as error:
            raise error
