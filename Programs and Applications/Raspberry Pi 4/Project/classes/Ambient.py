import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from adafruit_dht import DHT11

from time import sleep

from classes.Ergonomics import BackBlock


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
            
            val = round(MGGetPercentage(),1)
            if val == -1:
                return "<400 ppm"
            else:
                return str(val) + " ppm"
            

        def get_body_temperature():
            pin7 = AnalogIn(self.__object, MCP.P7)
            return str(round(pin7.voltage * 100, 1)) + "ºC"  # Value in ºC -- 10 mV / ºC -- 0V @ 0ºC
        
        pin0 = AnalogIn(self.__object, MCP.P0) # FD
        pin1 = AnalogIn(self.__object, MCP.P1) # TE
        pin2 = AnalogIn(self.__object, MCP.P2) # TD
        pin3 = AnalogIn(self.__object, MCP.P3) # FE
        
        
        x = pin0.voltage # FD
        pin0_weight = abs(279.480389818160 - 2.61723607558251e-14 * ((1.10737385648242e31*x + 7.88581493385428e31)**(0.5)))

        
        x = pin1.voltage # TE
        pin1_weight = abs(-9.6102705944221 + 1.10611278126408e-14 * ((1.68934147733667e31 - 5.07575820090584e30*x)**(0.5)))
        
        
        x = pin2.voltage # TD
        pin2_weight = abs(127.707749259173 - 6.0176851883592e-14 * ((4.82973979305029e29*x + 3.01484182509251e30)**(0.5)))
        
        
        x = pin3.voltage # FE
        pin3_weight = abs(-36.9996978788559 + 1.42903812645078e-13 * ((5.33779116432089e29 - 1.61890367155651e29*x)**(0.5)))
        
        
        return_array = (get_luminosity(), get_noise(), get_co2(), get_body_temperature(),
                        pin0_weight, pin1_weight, pin2_weight, pin3_weight)
    
        return return_array


class AmbientDHT11:
    
    def __init__(self):
        self.__ready = False 
        self.device = DHT11(board.D17)
        self.__ready = True

    def is_ready(self):
        print("ready: " + str(self.__ready))
        return self.__ready

    def get_data(self):
        try:
            temp_c = self.device.temperature
            temp_f = temp_c * (9 / 5) + 32
            hum = self.device.humidity
            return str(round(temp_c,1))+"ºC", temp_f, str(round(hum,1))+"%"
        except:
            return False

