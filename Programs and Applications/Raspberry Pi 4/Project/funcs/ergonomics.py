from time import sleep
from numpy import mean
from datetime import datetime


from classes.Ergonomics import *
from classes.File import File
from classes.Firebase import Firebase


def start_ergonomics(seat_sensor="HX711"):

    firebase = Firebase()

    # Initialize Back Data Sensors
    seat_block = _seat_initialize(seat_sensor)

    # Initialize Seat Data Sensors
    back_block = _back_initialize()

    # Initialize coprocessor
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
    n_values = 10

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
    flag_cloud = True
    flag_file = False
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if flag_cloud:

        # TODO: position logic
        bl, br, fl, fr = seat_data_mean
        tr, dr, tl, dl = back_data_mean

        position = None
        if ...:
            "position 1"
            position = 1
        elif ...:
            "position 2"
            position = 2
        elif ...:
            "position 3"
            position = 3
        elif ...:
            "position 4"
            position = 4
        elif ...:
            "position 5"
            position = 5
        elif ...:
            "position 6"
            position = 6
        elif ...:
            "position 7"
            position = 7
        elif ...:
            "position 8"
            position = 8
        else:
            position = "error"

        firebase.push_ergonomics_position_data(position, date)

    if flag_file:
        file = File("output/Ergonomic/test1.csv")
        file.write("Back_data_mean: {}, Seat_data_mean: {}".format(back_data_mean, seat_data_mean))
        pass
