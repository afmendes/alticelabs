from time import sleep
from numpy import mean
from datetime import datetime

from classes.Ergonomics import *
from classes.File import File
from classes.Firebase import Firebase

count = 0
prev_pos = None


def start_ergonomics(firebase, seat_sensor="HX711"):

    # Initialize Back Data Sensors
    print("Init seat")
    seat_block = _seat_initialize(seat_sensor)

    # Initialize Seat Data Sensors
    print("Init back")
    back_block = _back_initialize()

    # Initialize coprocessor
    print("Init coproc")
    _coprocessor(firebase, seat_block, back_block, seat_sensor)


# -------------------- Seat --------------------

def _seat_initialize(seat_sensor: str):
    return SeatBlock(seat_sensor)


def _seat_get_data(seat_block: SeatBlock):
    return seat_block.get_data()


# -------------------- Back --------------------

def _back_initialize():
    return BackBlock()


def _back_get_data(back_block: BackBlock):
    return back_block.get_data()


# ---------------- Coprocessor -----------------

def _coprocessor(firebase: Firebase, seat_block: SeatBlock, back_block: BackBlock, seat_sensor: str):
    n_values = 1
    print("X")

    while not seat_block.is_ready() and not back_block.is_ready():
        sleep(0.5)

    try:
        while True:
            values = []
            for i in range(n_values):
                back_data = _back_get_data(back_block)
                seat_data = _seat_get_data(seat_block)
                values.append((back_data, seat_data))

            back_data_mean = [
                mean([x[0][0] for x in values]),
                mean([x[0][1] for x in values]),
                mean([x[0][2] for x in values]),
                mean([x[0][3] for x in values]),
            ]
            seat_data_mean = [
                mean([x[1][0] for x in values]),
                mean([x[1][1] for x in values]),
                mean([x[1][2] for x in values]),
                mean([x[1][3] for x in values]),
            ]
            _send_data(firebase, back_data_mean, seat_data_mean)
    except Exception as e:
        print(e)
        start_ergonomics(seat_sensor)


def _send_data(firebase: Firebase, back_data_mean: list, seat_data_mean: list):
    global count, prev_pos
    flag_cloud = False
    flag_file = True
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    try:
            if flag_cloud:

                # TODO: position logic
                topo_dir, topo_esq, baixo_esq , baixo_dir  = back_data_mean
                tras_dir, tras_esq, frente_dir, frente_esq = seat_data_mean
                
                back_sum = sum(back_data_mean)
                seat_sum = sum(seat_data_mean)

                position = None
                
                tras_dir_perc = tras_dir / seat_sum * 100
                tras_esq_perc = tras_esq / seat_sum * 100
                frente_dir_perc = frente_dir / seat_sum * 100
                frente_esq_perc = frente_esq / seat_sum * 100
                
                if seat_sum < 5:
                    position = 9
                else:
                
                    if back_sum < 1000:
                        if frente_dir_perc + frente_esq_perc > 70:
                            position = 3
                        else:
                            position = 2
                    else:
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
                        elif tras_dir_perc > 40:
                            if frente_dir_perc < 13:
                                position = 7
                            else:
                                position = 5
                        elif tras_esq_perc > 60:
                            if frente_esq_perc < 5 and tras_esq > 25:
                                position = 8
                            else:
                                position = 6
                        elif abs(tras_esq_perc - tras_dir_perc) < 10:
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

                # firebase.push_ergonomics_position_data(position, date)
    except:
        ...
    if flag_file:
        
#         positions = [
#             "Posiçao 1 - Bem sentado / Normal",
#             "Posiçao 2 - Inclinado para a frente com as ancas bem posicionadas",
#             "Posiçao 3 - Inclinado para a frente com as ancas mal posicionadas",
#             "Posiçao 4 - Inclinado para trás com as ancas mal posicionadas",
#             "Posiçao 5 - Inclinado para o lado direito",
#             "Posiçao 6 - Inclinado para o lado esquerdo",
#             "Posiçao 7 - Perna direita cruzada",
#             "Posição 8 - Perna esquerda cruzada"
#         ]
#         positions = [
#             "-- Tras Dir --",
#             "-- Tras Esq --",
#             "-- Frente Dir --",
#             "-- Frente Esq --"
#         ]
#         count += 1

        topo_dir, topo_esq, baixo_esq, baixo_dir = back_data_mean

        tras_dir = seat_data_mean[0]
        tras_esq = seat_data_mean[1]
        frente_dir = seat_data_mean[2]
        frente_esq = seat_data_mean[3]
        sensor_str = "{:>8.1f}{:>8.1f}{:>8.1f}{:>8.1f}{:>20.3f}{:>8.3f}{:>8.3f}{:>8.3f}".format(
            topo_dir, baixo_dir, topo_esq, baixo_esq, tras_dir, tras_esq, frente_dir, frente_esq
        )
        
#         if count == 1:
#             sensor_str = "{:>8s}{:>8s}{:>8s}{:>8s}{:>20s}{:>8s}{:>8s}{:>8s}\n".format(
#             "TopoDir","BaixDir","TopoEsq","BaixEsq","TrasDir","TrasEsq","FrenDir","FrenEsq"
#         ) + sensor_str
#         if count % 5 == 1:
#             sensor_str = positions[int(count/5)] + "\n" + sensor_str
        
#         print(sensor_str)
        
#         if count % 5 == 0:
#             print("Counter: "+ str(count))
        
        # print("Back_data_mean: {}, Seat_data_mean: {}".format(back_data_mean, seat_data_mean))
        # Weights:  0.000kg,  2.850kg,  5.725kg, 7.725kg,
        #          10.235kg, 14.110kg, 16.110kg
        # Tras Dir, Tras Esq, Frente Dir, Frente Esq
        file = File("output/andre3.csv")
        file.write(sensor_str)
        # file.write("Back_data_mean: {}, Seat_data_mean: {}".format(back_data_mean, seat_data_mean))
        
        
#         if count >= 40:
#             exit(1)