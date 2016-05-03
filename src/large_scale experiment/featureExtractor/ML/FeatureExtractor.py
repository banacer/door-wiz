import numpy as np
from scipy.spatial import distance
speed = 3

def getAvgHeight(data):
    try:
        return np.mean(data[0<data[:,0],0])
    except ValueError:
        return 0

def getMaxHeight(data):
    try:
        return np.max(data[0<data[:,0],0])
    except ValueError:
        return 0

def getAvgWidth(data):
    try:
        return np.mean(data[0<data[:,1],1])
    except ValueError:
        return 0

def getMaxWidth(data):
    try:
        return np.max(data[0<data[:,1],1])
    except ValueError:
        return 0

def getcircumference(data,sampling_rate):
    try:
        beg = data[0,1]
        side = 0
        size = data[:,1].size
        previous_point = np.array([0,0])
        my_distance = timeToDistance(sampling_rate)
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
    
def timeToDistance(sampling_rate):
    try:
        distancePerMillisecond = float(speed) *100000 / (3600*1000)
        distance = 1000/sampling_rate * distancePerMillisecond
        return distance
    except ValueError:
        return 0