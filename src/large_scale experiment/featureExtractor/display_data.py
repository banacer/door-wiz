import re
from serial import Serial
import time

def run():
    ser = Serial('/dev/ttyACM0',9600)
    count = 0
    while True:
        line = ser.readline()
        #print line
        data = line.split(',')
        calibration_a = 0.01703217
        if len(data) != 3:
            continue
        for i in range(3):
             data[i] = calibration_a * float(data[i])
        print data[0], data[1], data[2]

if __name__ == '__main__':
    run()