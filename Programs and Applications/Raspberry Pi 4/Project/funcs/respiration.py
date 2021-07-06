from time import sleep, time
from datetime import datetime
from threading import Thread
import numpy as np
from scipy import signal, interpolate

from classes.Queue import Queue
from classes.File import File
from classes.Accelerometer import Respiration
from classes.Firebase import Firebase


def start_respiration():
    firebase = Firebase()

    # Initialize Respiration Rate Module
    respiration = _respiration_initialize()

    # Initialize coprocessor
    _coprocessor(firebase, respiration)


# -------------------- Respiration --------------------
def _respiration_initialize():
    return Respiration()


def _respiration_get_data(respiration: Respiration):
    return respiration.get_data()


def _respiration_filter(buffer: list):
    def find_outliers(data):
        """
        Find outliers in raw data and returns an array with 1s where the outliers are found
        If any point is outside of three times the deviation, is considered an outlier
        :param data:
        :return:
        """

        # Array of Falses
        outliers = [False] * len(data)

        # mean and standard deviation
        threshold = 3
        mean = np.mean(data)
        std = np.std(data)

        # Find outliers
        for index, point in enumerate(data):
            z_score = (point - mean) / std
            if np.abs(z_score) > threshold:
                outliers[index] = True

        return outliers

    def fill_missing(data):
        def find_first_number_index():
            ind = 0
            while True:
                if not np.isnan(data[ind]):
                    return ind
                else:
                    ind += 1

        def find_last_number_index():
            ind = len(data) - 1
            while True:
                if not np.isnan(data[ind]):
                    return ind
                else:
                    ind -= 1

        def find_next_number_index(ind):
            while True:
                if not np.isnan(data[ind]):
                    return ind
                else:
                    ind += 1

                if ind >= len(data):
                    return False

        def calc_line(point1, point2):
            m_ = (point2(0) - point1(0)) / (point2(1) - point1(1))
            b_ = point1(0) - m_ * point1(1)
            return m_, b_

        def fill(index1, index2):
            data1 = data[index1]
            data2 = data[index2]

            m_, b_ = calc_line((index1, data1), (index2, data2))

            for i in range(index1+1, index2, 1):
                data[i] = m_*i+b_




        first_number_index = find_first_number_index()

        last_number_index = find_last_number_index()

        data = data[first_number_index:last_number_index]

        prev_index = 0
        index_ = find_next_number_index(prev_index + 1)
        while index_:
            fill(prev_index, index_)
            prev_index = index_
            index_ = find_next_number_index(prev_index + 1)

        return data, first_number_index, last_number_index

    def filter_band_pass_iir(input_data, fs, N, lower_freq=0.1, upper_freq=0.6):
        """
        Apply an IIR Band-pass filter on input data
        :param input_data:
        :param fs:
        :param N:
        :param lower_freq:
        :param upper_freq:
        :return:
        """
        b, a = signal.iirfilter(N, [2 * np.pi * lower_freq, 2 * np * upper_freq], fs=fs, btype="band")
        output_data = signal.filtfilt(b, a, input_data)
        return output_data

    def smooth_data(data, date):
        f = interpolate.interp1d(date, data, kind="linear")
        date_int = np.linspace(date[0], date[-1], len(date))
        data_int = f(date_int)
        return data_int

    def local_maxima_count(data):
        a = np.array(data)
        maximas = signal.argrelextrema(a, np.greater)
        return len(maximas)

    data = buffer[0]
    date = buffer[1]
    frequencies = []

    prev_value = date[0]

    for value in date[1:]:
        frequencies.append(1/(value-prev_value))
        prev_value = value

    Fs = sum(frequencies)/len(frequencies)

    # Find outliers in data and remove them
    outliers = find_outliers(data)
    for index, val in enumerate(outliers):
        if val is True:
            data[index] = np.nan

    # Fill missing values in data
    data, first_number_index, last_number_index = fill_missing(data)
    date = date[first_number_index:last_number_index]

    # Filter data using an iir filter of 5th order
    data = filter_band_pass_iir(data, Fs, 5)

    data = smooth_data(data, date)

    count = local_maxima_count(data)

    return count/(date(-1)-date(0))*60


# ------------------ Coprocessor ----------------
def _coprocessor(firebase: Firebase, respiration: Respiration):

    while not respiration.is_ready():
        sleep(0.5)

    queue = Queue()
    buffer = []

    def read_data_thread():
        while True:
            queue.enqueue(_respiration_get_data(respiration))
            sleep(0.01)

    thread = Thread(target=read_data_thread, args=())
    thread.start()

    start_time = time()
    while True:
        if not queue.is_empty():
            buffer.append(queue.dequeue())
        if (time() - start_time) < 60:
            respiration_data = _respiration_filter(buffer)
            buffer = []
            _send_data(firebase, respiration_data)
            start_time = time()


def _send_data(firebase: Firebase, respiration_data):
    flag_cloud = True
    flag_file = False
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if flag_cloud:

        # Respiration
        firebase.push_ergonomics_body_respiration(respiration_data, date)

    if flag_file:
        ...
