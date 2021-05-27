from threading import Thread

"""from funcs.seat import start_seat
from funcs.mcp import start_mcp
from funcs.dht import start_dht
from funcs.accelerometer import start_accel
from funcs.optics import start_optics"""

# from classes.File import File
from classes.Cloud import Cloud
# from classes.Application import Application


def main():
    '''rasp_id = "6f96a294-2906-4c63-a13f-aeda7929f498"
    rasp_secret = "65s531g4q62eg94hqm7utr06o80h7vtumu6efsmgdfqsk9gaphir"'''

    rasp_id = "6f96a294-2906-4c63-a13f-aeda7929f498"
    rasp_secret = "65s531g4q62eg94hqm7utr06o80h7vtumu6efsmgdfqsk9gaphir"

    # Flags
    flag_debug = True
    flag_print = False
    flag_file = False
    flag_cloud = False

    # Components
    flag_mcp = False
    flag_hx711 = False
    flag_optics = False
    flag_dht = False
    flag_accel = False

    filepath_mcp = "output/MCP3008"
    filepath_hx711 = "output/HX711"
    filepath_optics = "output/OPTICS"
    filepath_dht = "output/DHT11"
    filepath_accel = "output/ACCELEROMETER"

    filename_mcp = "output.csv"
    filename_hx711 = "output.csv"
    filename_optics = "output.csv"
    filename_dht = "output.csv"
    filename_accel = "output.csv"

    # --------------- Cloud ---------------
    if flag_debug:
        print("Initializing cloud..")
    cloud = Cloud(rasp_id, rasp_secret)
    print(cloud.get_access_token())

    # --------------- Threads ---------------
    if flag_hx711:
        """seat_t = Thread(target=start_seat, args=(flag_debug, flag_print, flag_file, flag_cloud))
        seat_t.start()"""

    if flag_dht:
        """dht_t = Thread(target=start_dht, args=(flag_debug, flag_print, flag_file, flag_cloud))
        dht_t.start()"""

    if flag_mcp:
        """mcp_t = Thread(target=start_mcp, args=(flag_debug, flag_print, flag_file, flag_cloud))
        mcp_t.start()"""

    if flag_optics:
        """optics_t = Thread(target=start_optics, args=(flag_debug, flag_print, flag_file, flag_cloud))
        optics_t.start()"""

    if flag_accel:
        """accel_t = Thread(target=start_accel, args=(flag_debug, flag_print, flag_file, flag_cloud))
        accel_t.start()"""

















    """
    file = File("test.csv", "output")
    print(file.exists())
    file.create("YES")
    print(file.exists())
    file.write("123")
    file.write(321)
    file.write_list((123,321,123,321))
    file.write_list(("test","test2",123,321))
    """

main()