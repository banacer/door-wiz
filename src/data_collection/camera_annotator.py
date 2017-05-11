import argparse
import os
import sys
import time

import cv2
import matplotlib as mpl
import numpy as np

mpl.use('Agg')

import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, "..", ".."))
modelDir = '/home/cuda/bamos/models'#os.path.join(fileDir, '..', '..', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')


parser = argparse.ArgumentParser()
parser.add_argument('--dlibFacePredictor', type=str, help="Path to dlib's face predictor.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Path to Torch network model.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))
parser.add_argument('--imgDim', type=int,help="Default image dimension.", default=96)
parser.add_argument('--verbose', action='store_true', default=False)
args = parser.parse_args()

align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, imgDim=args.imgDim, cuda=False)

def processFrame(frame):
        # head = "data:image/jpeg;base64,"
        # assert(dataURL.startswith(head))
        # imgdata = base64.b64decode(dataURL[len(head):])
        # imgF = StringIO.StringIO()
        # imgF.write(imgdata)
        # imgF.seek(0)
        img = frame #Image.open(imgF)

        buf = np.fliplr(np.asarray(img))
        rgbFrame = np.zeros((300, 400, 3), dtype=np.uint8)
        rgbFrame[:, :, 0] = buf[:, :, 2]
        rgbFrame[:, :, 1] = buf[:, :, 1]
        rgbFrame[:, :, 2] = buf[:, :, 0]


        bb = align.getLargestFaceBoundingBox(rgbFrame)
        bbs = [bb] if bb is not None else []
        face = None
        for bb in bbs:
            # print(len(bbs))
            landmarks = align.findLandmarks(rgbFrame, bb)
            alignedFace = align.align(args.imgDim, rgbFrame, bb,
                                      landmarks=landmarks,
                                      landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
            if not alignedFace:
                continue
            else:
                #cv2.imshow('image',alignedFace)
                rep = net.forward(alignedFace)
                face = alignedFace
                # print(rep)
        return face

def getRep(bgrImg):
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


    cv2.imwrite('/home/cuda/face.png', alignedFace)
    start = time.time()
    rep = net.forward(alignedFace)
    if args.verbose:
        print("  + OpenFace forward pass took {} seconds.".format(time.time() - start))
        print("Representation:")
        print(rep)
        print("-----\n")
    return rep

if __name__ == '__main__':
    cap = cv2.VideoCapture('/home/cuda/workspace/experiment_data/videos/d1_03-20-17_10.avi')
    i = 0
    print int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    while(cap.isOpened()):
        #print 'hey'
        grabbed, frame = cap.read()
        if i%1000 == 0:
            print 'processed', i
        i+=1
        if not grabbed:
            break
        try:
            face = getRep(frame)
            print 'found face in ', i
        except Exception as e:
            #print e
            pass
    print 'done'