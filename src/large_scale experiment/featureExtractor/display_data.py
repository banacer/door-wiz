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
        calibration_a = .01877037
        if len(data) != 3:
            continue
        # for i in range(3):
        #      data[i] = calibration_a * float(data[i])
        print data[0], data[1], data[2]
        # print data[0], 216.65
        # print data[1], 114.94
        # print data[2].rstrip('\n\r'), 114.78

if __name__ == '__main__':
    run()