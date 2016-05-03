import re
from serial import Serial
import time
import numpy as np
import ML.FeatureExtractor as features
import threading
import Queue
import camera as mycamera
import os
import copy

#queue = Queue.Queue()
#camera_done = False

def get_height_and_width(data):
    measures = []
    measures.append(213.5 - float(data[0]))
    measures.append(112 - float(data[1]) - float(data[2]))
    return measures

def write_event_data(event_file, event_data, len, current_time):
    for i in range(0,len):
        event_file.write(str(event_data[i,0])+','+str(event_data[i,1])+'\n')
    event_file.write(str(current_time) + '_\n')
    event_file.flush()
"""
def get_video_events(video_id):
    print 'video_id: ' , video_id
    while not queue.empty():
        info = queue.get()
        print 'queue item: ', info
        if info[3] != video_id:
            queue.put(info)
            break
        video_time = info[4]
        my_start = info[0] - video_time - 1
        if my_start < 0:
            my_start = 0
        my_end = info[1] - video_time + 1
        if my_end > 10:
            my_end = 10
        event_id = info[2]
        mycamera.extract_video_event(my_start, my_end, event_id, video_id)
    #delete video
    print 'deleting ' + 'output' + str(video_id) + '.avi'
    os.remove('output'+str(video_id)+'.avi')

#A wrapper around the do_capture function in Camera module
def do_capture(id):
    global camera_done
    camera_done = False
    mycamera.do_capture(id)
    camera_done = True

def get_video_event():
    #Camera footage stuff
    video_time = time.time()
    video_id = 1
    camera_thread = threading.Thread(target=do_capture,args=(video_id,))
    #camera_thread.daemon = True
    camera_thread.start()
    video_id += 1
"""
def read_sensor_data():
    ser = Serial('/dev/ttyACM0',9600)
    count= 0
    temperature = 23
    calibration_a = 0.013696
    calibration_b = -3.56201
    event = []
    eventCount = 0
    event_id = num_lines = sum(1 for line in open('features.dat')) + 1
    all_data_file = open('all_data.dat','a')
    raw_event_file = open('event_raw.data', 'a')
    feature_file = open('features.dat','a')
    log_file = open('readline.log','a')
    event_time = []


    #Camera footage stuff
    #video_time = time.time()
    #video_id = 1
    #camera_thread = threading.Thread(target=do_capture,args=(int(video_id),))
    #camera_thread.daemon = True
    #camera_thread.start()
    #start reading sensory data
    while True:
        try:
            line = ser.readline()
            current_time = time.time()
            count +=1
            data = line.split(',')
            """
            #camera footage stuff
            if camera_done: # this means video shot finished

                #Extracting video from 1-minute long video
                subvideo_thread = threading.Thread(target=get_video_events,args=(int(video_id),))
                #subvideo_thread.daemon = True
                subvideo_thread.start()
                #Start new video
                video_id += 1
                video_time = time.time()
                camera_thread = threading.Thread(target=do_capture,args=(int(video_id),))
                #camera_thread.daemon = True
                camera_thread.start()
            """

            all_data_file.write(str(current_time)+','+line+'\n')
            all_data_file.flush()
            if len(data) == 3:
                for i in range(0,3):
                    val =re.sub('[^0-9]','', data[i])
                    #data[i] = int(val)#((float(val) / 10**4 ) * (331.3 + 0.606 * temperature)) / 2
                    data[i] = calibration_a * float(val) + calibration_b

                measures = get_height_and_width(data)

                if (110 < measures[0] and measures[0] < 200) or measures[1] > 20:  #start of passing event
                    #print "measures: ",measures
                    if eventCount == 0:
                        event_time = []
                        event_time.append(copy.copy(time.time()))
                    event.append(measures)
                    eventCount += 1
                elif eventCount > 5: # extract features
                    event_time.append(time.time())
                    eventdata = np.array(event)
                    avgHeight = features.getAvgHeight(eventdata)
                    maxHeight = features.getMaxHeight(eventdata)
                    avgWidth = features.getAvgWidth(eventdata)
                    maxWidth = features.getMaxWidth(eventdata)
                    circumference = features.getcircumference(eventdata, 50.0)
                    feature_line =  str(avgHeight)+','+ str(maxHeight)+','+ str(avgWidth)+ ','+ str(maxWidth) + ',' + str(circumference)
                    #print feature_line
                    feature_file.write(str(current_time)+','+feature_line+'\n')
                    feature_file.flush()
                    write_event_data(raw_event_file,eventdata,eventCount,current_time)

                    #save event id to structrure and increment event_id
                    event_time.append(copy.copy(event_id))
                    #event_time.append(copy.copy(video_id))
                    #event_time.append(copy.copy(video_time))
                    event_id += 1
                    #push event time to queue
                    #print 'pushing ', event_time
                    #queue.put(event_time)
                    #print 'queue size: ', queue._qsize()
                    #initialize vars for next event
                    eventCount = 0
                    event = []
                    event_time = []
        except Exception:
            t = time.time()
            print 'error'
            log_file.write('An error occured at ' + str(t))
            pass

#start program
read_sensor_data()
