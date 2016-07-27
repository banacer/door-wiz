import re
from serial import Serial
import time
from time import time
def run():
    ser = Serial('/dev/ttyACM0',9600)
    count = 0
    prev = time()
    max_height = 223
    max_width = 121
    while True:
        line = ser.readline().rstrip('\n\r')
        #print line
        data = line.split(',')
        calibration_a = .01877037
        if len(data) != 3:
            continue
        for i in range(3):
             data[i] = calibration_a * float(data[i])
        now = time()
        rate = 1/(now - prev)
        #print '{} {} {} {}'.format(data[0], data[1], data[2], data[3])
        print '{:5.2f} {:5.2f} {:5.2f} {:4.2f}'.format(max_height - data[0], data[1], data[2], rate)
        prev = now
        # print data[0], 216.65
        # print data[1], 114.94
        # print data[2].rstrip('\n\r'), 114.78

if __name__ == '__main__':
    run()