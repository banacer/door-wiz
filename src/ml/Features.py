"""
This class contains a set of functions to extract features from a
numpy array of a walking event
"""
import numpy as np
from scipy.spatial import distance as dist
from pandas import Series, DataFrame


def extract_mean_height(data):
    """
    Extracts mean height
    :param data: numpy array
    :return: returns mean as a scalar
    """
    try:
        if isinstance(data, DataFrame):
            return data['height'].mean()
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_min_max_height(data):
    """
    extract minimum and maximum height
    :param data: numpy array
    :return: min,max scalars
    """
    try:
        if isinstance(data, DataFrame):
            _min = data['height'].min()
            _max = data['height'].max()
            return _min, _max
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_mean_width(data):
    """
    extract mean width
    :param data: numpy array
    :return: mean width as scalar
    """
    try:
        if isinstance(data, DataFrame):
            return data['width'].mean()
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_min_max_width(data):
    """
    return minimum and maximum width
    :param data: numpy array
    :return: min,max scalars
    """
    try:
        if isinstance(data, DataFrame):
            _min = data['width'].min()
            _max = data['width'].max()
            return _min, _max
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_girth(data, sampling_rate, speed=5):
    """
    Computes waiste circumference aka girth

    :param data: numpy array
    :param sampling_rate: the sampling rate
    :param speed: default value 5 km/h
    :return: girth as scalar
    """
    try:
        if isinstance(data, DataFrame):
            beg = 0
            first = True
            my_distance = __convert_time(sampling_rate, speed)
            side = 0
            for idx, row in data[:-1].iterrows():
                if first:
                    beg = row['width']
                    first = False
                    first_idx = idx
                    previous_point = np.array([row['width'], 0])
                    continue
                if row['width'] < 0:
                    continue
                current_point = np.array([row['width'], (idx - first_idx) * my_distance])
                euclidean_distance = dist.euclidean(current_point, previous_point)
                previous_point = current_point
                side += euclidean_distance / 2
            end = data['width'].iloc[-1]
            circumference = beg + end + 2 * side
            return circumference
    except ValueError, exception:
        print exception
        return np.nan


def __convert_time(sampling_rate, speed):
    """
    helper function to get distance traveled per sampling time given speed
    :param sampling_rate: sampling rate
    :param speed: speed of person
    :return: distance traveled
    """
    try:
        distance_per_ms = float(speed) / 36
        distance = 1000 / sampling_rate * distance_per_ms
        return distance
    except ValueError:
        return np.nan

def extract_time(data, sampling_rate):
    """
    Extracts time spent under the door
    :param data: numpy array
    :param sampling_rate: sampling rate
    :return:
    """
    try:
        if isinstance(data, DataFrame):
            _min = int(data.index.min())
            _max = int(data.index.max())
            return (_max - _min) * 1000 / sampling_rate
        else:
            return np.nan
    except ValueError:
        return np.nan
