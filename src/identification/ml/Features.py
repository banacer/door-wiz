import numpy as np
from scipy.spatial import distance
from pandas import Series, DataFrame


def extract_mean_height(data):
    try:
        if isinstance(data, DataFrame):
            return data['height'].mean()
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_min_max_height(data):
    try:
        if isinstance(data, DataFrame):
            min = data['height'].min()
            max = data['height'].max()
            return min, max
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_mean_width(data):
    try:
        if isinstance(data, DataFrame):
            return data['width'].mean()
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_min_max_width(data):
    try:
        if isinstance(data, DataFrame):
            min = data['width'].min()
            max = data['width'].max()
            return min, max
        else:
            return np.nan
    except ValueError:
        return np.nan


def extract_girth(data, sampling_rate, speed=5):
    try:
        if isinstance(data,DataFrame):
            beg = 0
            first = True
            my_distance = __convert_time(sampling_rate,speed)
            side = 0
            for idx,row in data[:-1].iterrows():
                if first:
                    beg = row['width']
                    first = False
                    first_idx = idx
                    previous_point = np.array([row['width'], 0])
                    continue
                if row['width'] < 0:
                    continue
                current_point = np.array([row['width'], (idx - first_idx) * my_distance])
                euclidean_distance = distance.euclidean(current_point, previous_point)
                previous_point = current_point
                side += euclidean_distance / 2
            end = data['width'].iloc[-1]
            circumference = beg + end + 2 * side
            return circumference
    except ValueError,e:
         print e
         return np.nan


def __convert_time(sampling_rate, speed):
    try:
        distancePerMillisecond = float(speed) / 36
        distance = 1000 / sampling_rate * distancePerMillisecond
        return distance
    except ValueError:
        return np.nan

def extract_time(data,sampling_rate,speed=5):
    try:
        if isinstance(data,DataFrame):
            min = int(data.index.min())
            max = int(data.index.max())
            return (max - min) * 1000/sampling_rate
        else:
            return np.nan
    except ValueError:
        return np.nan

def is_prime(num):
    for i in range(2,num):
        if num % i == 0:
            return False
    return True