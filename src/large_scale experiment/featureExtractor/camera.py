#import numpy as np
import cv2
import time
import os.path

def do_capture(id):
    cap = cv2.VideoCapture(0)
    #cap.set(cv2.cv.CV_CAP_PROP_FPS, 20)
    # Define the codec and create VideoWriter object
    # fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    fourcc = cv2.cv.CV_FOURCC('H','2','6','4')
    out = cv2.VideoWriter('output'+str(id)+'.h264', fourcc, 10.0, (320, 240))
    start = time.time()
    current = time.time()
    count = 1
    while current - start < 10:
        print count
        count += 1
        print (current - start)
        ret, frame = cap.read()
        current = time.time()
        if ret == True:
            pass
            # write the flipped frame
            out.write(frame)

            #cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return start



def extract_video_event(start, end, video, id):
    print 'nice!' , str(start), ' , ' , str(end) , ' , ' , str(id)
    inputfile = 'output'+str(id)+'.avi'
    print inputfile
    if not os.path.isfile(inputfile):
        print 'file not found'
        return
    cap = cv2.VideoCapture(inputfile)

    nFrames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT ) )
    fps = nFrames / 10
    fourcc = cv2.cv.CV_FOURCC('H','2','6','4')
    out = cv2.VideoWriter('videos/'+ str(video) + '.avi', fourcc, 4.0, (640, 480))
    f_start = start * fps
    f_end = end * fps
    print nFrames
    print fps
    print f_start
    print f_end

    for count in xrange( nFrames ):
        ret, frame = cap.read()
        #print 'count: ' + str(count)
        if f_start <= count and count <= f_end:
            out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


#do_capture(12)
#extract_video_event(2, 5, 'video.avi')
