from time import sleep, time
from datetime import datetime
from numpy import mean

from classes.File import File
from classes.Ambient import *
from classes.Ergonomics import *
from classes.Firebase import Firebase

count = 0
prev_pos = None


def start_ambient(firebase, all_in_one = False):

    # Initialize DHT11 Sensor
    dht = _dht11_initialize()

    # Initialize MCP3008 ADC
    mcp = _mcp3008_initialize()
    
    if all_in_one:
#         mcp2 = _mcp3008_initialize_2()
        mcp2 = _back_initialize()
    else:
        mcp2 = False

    # Initialize coprocessor
    _coprocessor(firebase, dht, mcp, mcp2, all_in_one)


# -------------------- DHT11 --------------------
def _dht11_initialize():
    return AmbientDHT11()


def _dth11_get_data(dht: AmbientDHT11):
    return dht.get_data()


# ------------------- MCP3008 -------------------
def _mcp3008_initialize():
    return AmbientMCP3008()


def _mcp3008_get_data(mcp: AmbientMCP3008):
    return mcp.get_data()


# -------------------- Back --------------------
def _back_initialize():
    return BackBlock()


def _back_get_data(back_block: BackBlock):
    return back_block.get_data()


# ------------------ Coprocessor ----------------
def _coprocessor(firebase: Firebase, dht: AmbientDHT11,
                 mcp: AmbientMCP3008, mcp2: BackBlock, all_in_one: bool):

    n_values = 5  # n values used for average
    values = []  # values array for averaging
    counter = 0  # counter used of printing and debugging

    while not dht.is_ready() and not mcp.is_ready():
        sleep(0.5)

    try:
        while True:
            start_time = time()

            # retrieve data from dht11
            dht_data = _dth11_get_data(dht)
#             print("dht: " + str(dht_data))

            # retrieve data from mcp3008
            mcp_data = _mcp3008_get_data(mcp)
#             print("mcp: " + str(mcp_data))

            # if all_in_one is active, it also retrieves the data from BackBlock and SeatBlock with optics
            if all_in_one:
                counter += 1
                # retrieve data from BackBlock
                back_data = _back_get_data(mcp2)
#                 print("back: " + str(back_data))
                values.append([back_data, mcp_data[4:8]])
            else:
                back_data = None

#             while (time() - start_time) < 5:
#                 sleep(0.1)
#
#             if
            if counter >= n_values:
                counter = 0
                # retrieves back data from x array
                back_data = [
                    mean([x[0][0] for x in values]),
                    mean([x[0][1] for x in values]),
                    mean([x[0][2] for x in values]),
                    mean([x[0][3] for x in values]),
                ]
                # retrieves seat data from x array
                seat_data = [
                    mean([x[1][2] for x in values]), # TD
                    mean([x[1][1] for x in values]), # TE
                    mean([x[1][0] for x in values]), # FD
                    mean([x[1][3] for x in values]), # FE
                ]
                values = []
                _send_data(firebase, dht_data, mcp_data, [back_data, seat_data], all_in_one)
            else:
                _send_data(firebase, dht_data, mcp_data, [],
                           all_in_one)
    except Exception as e:
        print(e)
        start_ambient(firebase)


def _send_data(firebase: Firebase, dht_data, mcp_data, values, all_in_one: bool):
    global count, prev_pos
    flag_cloud = True  # cloud flag used to send data to Firebase
    flag_file = False  # file flag used for debugging

    # get current timestamp
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    try:
        if flag_cloud:

            # DHT11
            if dht_data:
                temperature = dht_data[0]
                humidity = dht_data[2]
                firebase.push_dht_data(temperature, humidity, date)

            # MCP1
            luminosity, noise, co2_read, body_temperature = mcp_data[0:4]
            firebase.push_mcp_data(luminosity, co2_read, noise, date)
            firebase.push_ergonomics_body_temperature(body_temperature, date)

            # if all_in_one active, process ergonomics related data
            if all_in_one and values:
                topo_dir, topo_esq, baixo_esq, baixo_dir = values[0]
                tras_dir, tras_esq, frente_dir, frente_esq = values[1]

                # sum of each block of data
                back_sum = sum(values[0])
                seat_sum = sum(values[1])

                position = None

                # individual percentages of seat sensors
                tras_dir_perc = tras_dir / seat_sum * 100
                tras_esq_perc = tras_esq / seat_sum * 100
                frente_dir_perc = frente_dir / seat_sum * 100
                frente_esq_perc = frente_esq / seat_sum * 100

                # Logic used to determine position detected
                if seat_sum < 15:
                    position = 9
                else:
                
                    if back_sum < 1000:
                        if frente_dir_perc + frente_esq_perc > 80:
                            position = 3
                        else:
                            position = 2
                    else:
                        # individual percentages of backrest sensors
                        topo_dir_perc = topo_dir / back_sum * 100
                        topo_esq_perc = topo_esq / back_sum * 100
                        baixo_esq_perc = baixo_esq / back_sum * 100
                        baixo_dir_perc = baixo_dir / back_sum * 100
                        if topo_dir_perc + topo_esq_perc < 5:
                            position = 2
                        # Lower back not in the right position  
                        elif baixo_esq_perc + baixo_dir_perc < 10:
                            position = 4
                        elif (topo_esq_perc < 5) and (topo_dir_perc + baixo_dir_perc > 50):
                            position = 5
                        elif (topo_dir_perc < 5) and (topo_esq_perc + baixo_esq_perc > 50):
                            position = 6
                        elif tras_dir_perc > 25:
                            if frente_dir_perc < 20:
                                position = 7
                            else:
                                position = 5
                        elif tras_esq_perc > 40:
                            if frente_esq_perc < 35:
                                position = 8
                            else:
                                position = 6
                        elif abs(tras_esq_perc - tras_dir_perc) < 5:
                            position = 5
                        else:
                            position = 1
                
                positions = [
                    "Posiçao 1 - Bem sentado / Normal",
                    "Posiçao 2 - Inclinado para a frente com as ancas bem posicionadas",
                    "Posiçao 3 - Inclinado para a frente com as ancas mal posicionadas",
                    "Posiçao 4 - Inclinado para trás com as ancas mal posicionadas",
                    "Posiçao 5 - Inclinado para o lado direito",
                    "Posiçao 6 - Inclinado para o lado esquerdo",
                    "Posiçao 7 - Perna direita cruzada",
                    "Posição 8 - Perna esquerda cruzada",
                    "Posição x - Ninguém está sentado"
                ]
                            
                print("Position detected: " + positions[position-1])
                
                if prev_pos == position:
                    firebase.push_ergonomics_position_data(position, date)
                else:
                    prev_pos = position
                
    except:
        ...

    # if condition used for data debugging
    if flag_file:
        if all_in_one and values:
        
            positions = [
                "Posiçao 1 - Bem sentado / Normal",
                "Posiçao 2 - Inclinado para a frente com as ancas bem posicionadas",
                "Posiçao 3 - Inclinado para a frente com as ancas mal posicionadas",
                "Posiçao 4 - Inclinado para trás com as ancas mal posicionadas",
                "Posiçao 5 - Inclinado para o lado direito",
                "Posiçao 6 - Inclinado para o lado esquerdo",
                "Posiçao 7 - Perna direita cruzada",
                "Posição 8 - Perna esquerda cruzada"
            ]
            
            count += 1

            topo_dir, topo_esq, baixo_esq, baixo_dir = values[0]
            tras_dir, tras_esq, frente_dir, frente_esq = values[1]
            
            sensor_str = "{:>8.1f}{:>8.1f}{:>8.1f}{:>8.1f}{:>20.3f}{:>8.3f}{:>8.3f}{:>8.3f}".format(
                topo_dir, baixo_dir, topo_esq, baixo_esq, tras_dir, tras_esq, frente_dir, frente_esq
            )
            
#             if count == 1:
#                 sensor_str = "{:>8s}{:>8s}{:>8s}{:>8s}{:>20s}{:>8s}{:>8s}{:>8s}\n".format(
#                 "TopoDir","BaixDir","TopoEsq","BaixEsq","TrasDir","TrasEsq","FrenDir","FrenEsq"
#             ) + sensor_str
#             if count % 5 == 1:
#                 sensor_str = positions[int(count/5)] + "\n" + sensor_str           
            
#             print("Counter: "+ str(count))
            print(sensor_str)
            
            # print("Back_data_mean: {}, Seat_data_mean: {}".format(back_data_mean, seat_data_mean))
            # Weights:  0.000kg,  2.850kg,  5.725kg, 7.725kg,
            #          10.235kg, 14.110kg, 16.110kg
            # Tras Dir, Tras Esq, Frente Dir, Frente Esq
#             file = File("output/Andre.txt")
#             file.write(sensor_str)
            # file.write("Back_data_mean: {}, Seat_data_mean: {}".format(back_data_mean, seat_data_mean))
            
            
#         if count >= 40:
#             exit(1)
        else:
#             print("""
#             DHT11: {}
#             MCP3008: {}""".format(dht_data, mcp_data))
            ...
