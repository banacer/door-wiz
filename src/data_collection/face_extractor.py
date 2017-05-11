import argparse
import os
import math
import time
import cv2
import itertools
import os
import datetime

import numpy as np
np.set_printoptions(precision=2)
import openface
from multiprocessing import Pool
from src.utils import Utils
from sklearn.cluster import KMeans
import pickle

start = time.time()
fileDir = os.path.dirname(os.path.realpath(__file__))
#modelDir = os.path.join(fileDir, '..', 'models')
modelDir = '/home/cuda/bamos/models'#os.path.join(fileDir, '..', '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

parser = argparse.ArgumentParser()

#parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,
                    help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true', default=True)
parser.add_argument('--mongo_ip', type=str, default='172.26.56.122')
parser.add_argument('--mongo_port', type=int, default=27017)
parser.add_argument('--processes', type=int, default=250)
args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim, cuda=True)
if args.verbose:
    print("Loading the dlib and OpenFace models took {} seconds.".format(
        time.time() - start))


args = parser.parse_args()

def getRep((bgrImg, path)):
    if bgrImg is None:
        raise Exception("Unable to load image")
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)

    if args.verbose:
        print("  + Original size: {}".format(rgbImg.shape))

    start = time.time()
    bb = align.getLargestFaceBoundingBox(rgbImg)

    if bb is None:
        raise Exception("Unable to find a face")
    if args.verbose:
        print("  + Face detection took {} seconds.".format(time.time() - start))

    start = time.time()
    alignedFace = align.align(args.imgDim, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)


    if alignedFace is None:
        raise Exception("Unable to align image")
    if args.verbose:
        print("  + Face alignment took {} seconds.".format(time.time() - start))


    cv2.imwrite(path, alignedFace)
    #start = time.time()
    #rep = net.forward(alignedFace)
    # if args.verbose:
    #     print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
    #     print("Representation:")
    #     print(rep)
    #     print("-----\n")
    # return rep

def parse_img(alignedFace):
    start = time.time()
    rep = net.forward(alignedFace)
    if args.verbose:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(len(rep))
        print("-----\n")
    return rep

def run_face_extraction(iterable, face_link, video_link):
    calibration = 95+27
    processes = args.processes
    pool = Pool(processes=processes, maxtasksperchild=100)
    pool.daemon = True
    skip = True
    files = [filename for filename in os.listdir(face_link)]
    id = [file[:24] for file in files]
    parsed = set(id)
    for i, item in enumerate(iterable):
        if str(item['_id']) == '58dd5bf05c4e323398440e60':
            skip = False
        if skip:
            print 'here', i
            continue
        if item['_id'] in parsed:
            print 'skipping'
            continue
        print 'now here', str(item['_id'])
        file_name = datetime.datetime.fromtimestamp(item['time']).strftime("%m-%d-%y_%H")
        door_id = item['door']
        file_name = video_link + door_id + '_' + file_name + '.avi'
        print i, item['door'], datetime.datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M:%S')
        print item['_id']
        if int(datetime.datetime.fromtimestamp(item['time']).strftime('%H')) > 22:
            continue
        d = datetime.datetime.fromtimestamp(item['time'])
        newdate = d.replace(minute=0, second=0).strftime('%s')
        event_time = int(item['time']) - int(newdate) - calibration
        if os.path.exists(file_name):
            cap = cv2.VideoCapture(file_name)
            length = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            fps = length / 3600
            start = (event_time - 2.5) * fps
            end = (event_time + 2.5) * fps
            print length, start, end
            cap.set(1, start)
            photo_id = 1
            frames = []
            paths = []
            for _ in range(int(math.floor(start)), int(math.ceil(end))):
                # print 'here',
                grabbed, frame = cap.read()
                frames.append(frame)
                path = face_link + str(item['_id']) + '_' + str(photo_id) + '.png'
                paths.append(path)
                photo_id += 1
                if not grabbed:
                    print 'not grabbed'
                    break
            try:
                pars = zip(frames, paths)
                pool.map(getRep, pars)
            except Exception as e:
                print e

def run_face_clustering(facelink):
    files = [filename for filename in os.listdir(facelink)]
    id = [file[:24] for file in files]
    reps = []
    for file in files:
        img = cv2.imread(facelink+file)
        rep = parse_img(img)
        reps.append(rep)
    return reps
if __name__ == '__main__':
    mongo_ip = args.mongo_ip
    mongo_port = args.mongo_port
    db = Utils.init_mongo_client(mongo_ip, mongo_port)
    collection_name = 'door_data'
    iterable = db[collection_name].find(no_cursor_timeout=True)
    video_link = '/home/cuda/workspace/experiment_data/videos/'
    face_link = '/home/cuda/workspace/experiment_data/faces_v2/'
    #run_face_extraction(iterable, face_link, video_link)
    reps = run_face_clustering(face_link)
    pickle.dump(reps, open(face_link+"save.p", "wb"))
    X = np.array(reps)
    kmeans = KMeans(n_clusters=70, random_state=0).fit(X)
    print kmeans.labels_