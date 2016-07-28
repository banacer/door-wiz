from serial import Serial
from time import time

calibration = .01877037
def run(port, max_height=223, max_width=123):
    ser = Serial(port, 9600)
    prev = time()
    while True:
        line = ser.readline().rstrip('\n\r')
        data = line.split(',')

        if len(data) != 3:
            continue
        for i in range(3):
            try:
                data[i] = calibration * float(data[i])
            except ValueError:
                continue
        now = time()
        rate = 1 / (now - prev)
        ut = data[0]
        ul = data[1]
        ur = data[2]
        width = 0
        height = max_height - ut
        if not (ul > 120 and ur > 120):
            width = max_width - ul - ur
        #print '{:5.2f} {:5.2f} {:5.2f} {:5.2f} {:4.2f}'.format(height, ul, ur, width, rate)
        prev = now

if __name__ == '__main__':
    run(port='/dev/ttyACM0')
