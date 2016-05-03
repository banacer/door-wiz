import numpy as np
import sys

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


def get_data():
    my_array = []
    for line in sys.stdin:
        line = line.split(',')
        for index, item in enumerate(line):
            item = item.replace("'", "").replace("[", "").replace("]", "")
            line[index] = float(item)
        my_array.append(line)
    data = np.array(my_array)
    return data

#def compute_DBSCAN(data):
def compute_DBSCAN(data):
    for i in range(0,5):
        for j in range(0,5):
            for k in range(0,5):
                if not(i == j == k):
                    X = data[:,[i,j,k]]
                    # Compute DBSCAN
                    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
                    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
                    core_samples_mask[db.core_sample_indices_] = True
                    labels = db.labels_
                    # Number of clusters in labels, ignoring noise if present.
                    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
                    if n_clusters_ != 0:
                        print i,',',j,',',k
                        print('Estimated number of clusters: %d' % n_clusters_)


arr = get_data()
arr = StandardScaler().fit_transform(arr)
compute_DBSCAN(arr)