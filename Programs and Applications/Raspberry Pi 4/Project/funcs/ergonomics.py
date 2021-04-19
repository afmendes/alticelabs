from threading import Thread


def start_ergonomics(
        flag_debug=False, flag_print=False, flag_cloud=True, flag_file=False,
        seat_sensor="SO"):

    # Initialize Back Data Sensors
    __seat_initialize()
    # TODO: implement it bitch

    # Initialize Seat Data Sensors
    __back_initialize()
    # TODO: implement it bitch

    # Initialize coprocessor
    __coprocessor()
    # TODO: implement it bitch
    pass


# -------------------- Seat --------------------

def __seat_initialize():
    # TODO: implement it bitch
    pass


def __seat_get_data():
    # TODO: implement it bitch
    pass


# -------------------- Back --------------------

def __back_initialize():
    print("You lied bitch")
    # TODO: implement it bitch
    pass


def __back_get_data():
    # TODO: implement it bitch
    pass


# ---------------- Coprocessor -----------------


def __coprocessor(
        flag_debug=False, flag_print=False, flag_cloud=True, flag_file=False,
        seat_sensor="SO"):
    # TODO: implement it bitch
    pass
