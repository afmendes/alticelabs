import smbus
from time import time


# respiration accelerometer class
class Respiration:
    # class initializer
    def __init__(self):
        self.__ready = False
        self.__bus = None
        self.__init_respiration()

    # return ready state of the accelerometer
    def is_ready(self):
        return self.__ready

    # initialize accelerometer respiration bus (1D address)
    def __init_respiration(self):
        # Get I2C bus
        self.__bus = smbus.SMBus(1)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x00(00)  StandBy mode
        self.__bus.write_byte_data(0x1D, 0x2A, 0x00)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x01(01)  Active mode
        self.__bus.write_byte_data(0x1D, 0x2A, 0x01)

        # MMA8452Q address, 0x1C(28)
        # Select Configuration register, 0x0E(14)
        # 0x00(00)  Set range to +/- 2g
        self.__bus.write_byte_data(0x1D, 0x0E, 0x00)
        self.__ready = True

    # returns z axis data obtained on the accelerometer with timestamp
    def get_data(self):
        # MMA8452Q address, 0x1d(28)
        # Read data back from 0x00(0), 7 bytes
        # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
        data = self.__bus.read_i2c_block_data(0x1D, 0x00, 7)

        z_accel = (data[5] * 256 + data[6]) / 16
        if z_accel > 2047:
            z_accel -= 4095

        date = time()

        return z_accel, date


# cardiac accelerometer class
class Heartbeat:
    # class initializer
    def __init__(self):
        self.__ready = False
        self.__bus = None
        self.__init_heartbeat()

    # return ready state of the accelerometer
    def is_ready(self):
        return self.__ready

    # initialize accelerometer cardiac bus (1C address)
    def __init_heartbeat(self):
        # Get I2C bus
        self.__bus = smbus.SMBus(1)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x00(00)  StandBy mode
        self.__bus.write_byte_data(0x1C, 0x2A, 0x00)

        # MMA8452Q address, 0x1C(28)
        # Select Control register, 0x2A(42)
        # 0x01(01)  Active mode
        self.__bus.write_byte_data(0x1C, 0x2A, 0x01)

        # MMA8452Q address, 0x1C(28)
        # Select Configuration register, 0x0E(14)
        # 0x00(00)  Set range to +/- 2g
        self.__bus.write_byte_data(0x1C, 0x0E, 0x00)
        self.__ready = True

    # returns z axis data obtained on the accelerometer with timestamp
    def get_data(self):
        # MMA8452Q address, 0x1d(28)
        # Read data back from 0x00(0), 7 bytes
        # Status register, X-Axis MSB, X-Axis LSB, Y-Axis MSB, Y-Axis LSB, Z-Axis MSB, Z-Axis LSB
        data = self.__bus.read_i2c_block_data(0x1C, 0x00, 7)

        z_accel = (data[5] * 256 + data[6]) / 16
        if z_accel > 2047:
            z_accel -= 4095

        date = time()

        return z_accel, date
