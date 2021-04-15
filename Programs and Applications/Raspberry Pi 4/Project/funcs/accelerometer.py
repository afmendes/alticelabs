import numpy as np
from scipy import signal, fft


# TODO: complete code for data acquire
def start_accel(flag_debug, flag_print, flag_file, flag_cloud, filename, filepath):
    pass


# TODO: complete code clean_data
def clean_data(data):

    # VARS
    fs = 100
    bpm_low_freq = 0.7
    bpm_high_freq = 10
    rr_low_freq = 0.1
    rr_high_freq = 0.6

    # Find outliers in data and remove them
    outliers = find_outliers(data)
    for index, val in enumerate(outliers):
        if val is True:
            data[index] = np.nan

    # Fill missing values in data
    data = fill_missing(data)





    pass


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

    def find_next_nan(ind):
        while True:
            if np.isnan(data[ind]):
                return ind, data[ind]
            else:
                ind += 1

            if ind >= len(data):
                return False, False

    def find_next_number(ind):
        while True:
            if not np.isnan(data[ind]):
                return ind, data[ind]
            else:
                ind += 1

            if ind >= len(data):
                return False, False

    def calc_line(point1, point2):
        m_ = (point2(0) - point1(0)) / (point2(1) - point1(1))
        b_ = point1(0) - m_ * point1(1)
        return m_, b_

    first_number_index = find_first_number_index()

    last_number_index = find_last_number_index()

    data = data[first_number_index:last_number_index]




def filter_band_pass_iir(input_data, fs, N, lower_freq, upper_freq):
    """
    Apply an IIR Band-pass filter on input data
    :param input_data:
    :param fs:
    :param N:
    :param lower_freq:
    :param upper_freq:
    :return:
    """
    b, a = signal.iirfilter(N, [2*np.pi*lower_freq, 2*np*upper_freq], fs=fs, btype="band")
    output_data = signal.filtfilt(b, a, input_data)
    return output_data


def rolling_data_segmentation(data, window_size, window_rolling):

    length = len(data)
    output = []

    start = 0
    end = window_size

    flag = True

    while flag:

        output.append(data[start:end])
        start += window_rolling
        end += window_size

        if end > length:
            output.append(data[start::])
            flag = False

    return output


def hamming_window(data):
    """
    Returns data applied with hamming window
    :param data:
    :return:
    """
    HammingWnd = signal.windows.hamming(len(data))
    data_HammingWnd = np.multiply(data, HammingWnd)
    return data_HammingWnd


def hilbert_transform(data):
    output_data = signal.hilbert(data)
    return output_data


def fourier_transform(data):
    output_data = fft.fft(data)
    return output_data
