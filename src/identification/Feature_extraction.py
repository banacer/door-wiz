'''
This module converts a "walking through the door" event to a row
with a set of features such as avg, min, max height, width, girth...
'''
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from scipy.spatial import distance

MAX_HEIGHT = 203
MAX_WIDTH = 142
SPEED = 3
SAMPLING_RATE = 15

def convert_file_to_data_frame(filename, id):
    '''
    This function takes a file in the form
    UR=<>
    UL=<>
    UT=<>
    and converts it to a numpy array
    :param filename: the path to the file
    :param id: the user identifier
    :return: a numpy array of the event
    '''
    my_file = open(filename,'r')
    lines = my_file.readlines()
    dict = {}
    data = []
    for line in lines:
        key = line.split('=')[0].rstrip()
        val = line.split('=')[1].rstrip()
        if dict.has_key(key):
            # we probably have all of them at this point
            height = MAX_HEIGHT - dict['UT']
            width = 0
            if dict.has_key('UL') and dict.has_key('UR'):
                if dict['UL'] > 140 or dict['UR'] > 140:
                    width = 0
                else:
                    width = MAX_WIDTH - dict['UL'] - dict['UR']
            data.append([height,width])
            dict = {}
        else:
            dict[key] = float(val)
    frame = DataFrame(data,columns=['height','width'])
    frame['id'] = id
    return frame

def get_frame(path):
    #path = '../../data/'
    result = []
    for id in range(1, 21):
        filename = path + 'u%d.dat' % id
        frame = convert_file_to_data_frame(filename, id)
        result.append(frame)
    frame = pd.concat(result)
    return frame


def get_avg_height(data):
    try:
        return np.mean(data[0<data[:,0],0])
    except ValueError:
        return 0

def get_max_height(data):
    try:
        return np.max(data[0<data[:,0],0])
    except ValueError:
        return 0

def get_avg_width(data):
    try:
        return np.mean(data[0<data[:,1],1])
    except ValueError:
        return 0

def get_max_width(data):
    try:
        return np.max(data[0<data[:,1],1])
    except ValueError:
        return 0

def get_circumference(data, sampling_rate):
    try:
        beg = data[0,1]
        side = 0
        size = data[:,1].size
        previous_point = np.array([0,0])
        my_distance = time_to_distance(sampling_rate)
        for i in range(1,size - 1):
            if data[i,1] < 0:
                continue
            current_point = np.array([data[i,1],i*my_distance])
            #print "C: ", current_point," , P: ",previous_point
            euclidean_distance = distance.euclidean(current_point, previous_point)
            previous_point = current_point
            if euclidean_distance > 5:
                continue

            side += euclidean_distance/2
            #print "euclidean distance: ", euclidean_distance, " side: " , side

        end = data[size - 1,1]
        circumference = beg + end + 2 * side
        return circumference
    except ValueError:
        return 0

def time_to_distance(sampling_rate):
    try:
        distancePerMillisecond = float(SPEED) * 100000 / (3600 * 1000)
        distance = 1000/sampling_rate * distancePerMillisecond
        return distance
    except ValueError:
        return 0

frame = get_frame()
frame['event'] = -1
res = frame[(frame['height'] > 1) & (frame['id'] == 1) & (frame['width'] > 10)]
res['index'] = res.index
res['delta'] = (res['index']-res['index'].shift()).fillna(0)
for row in res.iterrows():
    print row['delta']
