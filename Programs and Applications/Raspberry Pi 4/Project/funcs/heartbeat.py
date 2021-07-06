from time import sleep, time
from datetime import datetime
from threading import Thread
from scipy.fftpack import fft
from scipy import signal
import numpy as np

from classes.Queue import Queue
from classes.File import File
from classes.Accelerometer import Heartbeat
from classes.Firebase import Firebase


def start_hearbeat():
    firebase = Firebase()

    # Initialize Respiration Rate Module
    heartbeat = _heartbeat_initialize()

    # Initialize coprocessor
    _coprocessor(firebase, heartbeat)


# -------------------- Heartbeat --------------------
def _heartbeat_initialize():
    return Heartbeat()


def _heartbeat_get_data(heartbeat: Heartbeat):
    return heartbeat.get_data()


def _heartbeat_filter(buffer: list):
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

    def filter_band_pass_iir(input_data, fs, N, lower_freq=0.7, upper_freq=10):
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

    def estimate_heartbeat(data, Fs):
        n = len(data)
        y = np.array(data)
        yf = fft(y)
        xf = np.linspace(0.0, 1.0/2.0 * Fs, int(n/2))

        yf_abs = 2.0/n * np.abs(yf[:n//2])

        index = 0
        max = 0

        for index_, val in enumerate(yf_abs):
            if val > max:
                index = index_
                max = val

        return xf[index]

    def confidence(data, Fs):

        def condition_lower(f):
            index = 0
            while True:
                if f[index] > 0.7:
                    return index
                index += 1

        def condition_upper(f):
            index = len(f)
            while True:
                if f[index] < 10:
                    return index
                index -= 1

        n = len(data)
        y = np.array(data)
        yf = fft(y)
        xf = np.linspace(0.0, 1.0/2.0 * Fs, int(n/2))
        lower_index = condition_lower(xf)
        upper_index = condition_upper(xf)

        yf_abs = 2.0/n * np.abs(yf[:n//2])

        m = max(yf_abs[lower_index:upper_index])
        trap = (np.trapz(xf[lower_index:upper_index], yf_abs[lower_index:upper_index]))
        return m / (trap / 9.3)



    data = buffer[0]
    date = buffer[1]
    frequencies = []

    prev_value = date[0]

    for value in date[1:]:
        frequencies.append(1 / (value - prev_value))
        prev_value = value

    Fs = sum(frequencies) / len(frequencies)

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

    if confidence(data, Fs) > 25:
        return estimate_heartbeat(data, Fs)
    else:
        return 0


# ------------------ Coprocessor ----------------
def _coprocessor(firebase: Firebase, heartbeat: Heartbeat):

    while not heartbeat.is_ready():
        sleep(0.5)

    queue = Queue()
    buffer = []

    def read_data_thread():
        while True:
            queue.enqueue(_heartbeat_get_data(heartbeat))
            sleep(0.01)

    thread = Thread(target=read_data_thread, args=())
    thread.start()

    start_time = time()
    while True:
        if not queue.is_empty():
            buffer.append(queue.dequeue())
        if (time() - start_time) < 10:
            heartbeat_data = _heartbeat_filter(buffer)
            buffer = []
            _send_data(firebase, heartbeat_data)
            start_time = time()


def _send_data(firebase: Firebase, heartbeat_data):
    flag_cloud = True
    flag_file = False
    date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    if flag_cloud:
        # Heartbeat
        firebase.push_ergonomics_body_bpm(heartbeat_data, date)

    if flag_file:
        ...
