import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from scipy.spatial import distance
import ml.Features as ft
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn import decomposition  # PCA
from sklearn.metrics import confusion_matrix

if __name__ == '__main__':
    # we setup needed params
    MAX_HEIGHT = 203
    MAX_WIDTH = 142
    SPEED = 3
    SAMPLING_RATE = 8

    # setting up MQTT subscriber
