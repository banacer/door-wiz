from serial import Serial
import time
import re

ser = Serial('/dev/ttyACM0',9600)
start = time.time();
count= 0
sensors = []
while True:
    try:
        line = ser.readline()
        data = line.split(',')
        index = int(re.sub('[^0-9]','', data[0]))
        val = int(re.sub('[^0-9]','', data[1]))
        sensors[index - 1] = val
        if index == 2:
            t = time.time()
            print t,sensors[0],sensors[1],sensors[2]
    except:
        pass
