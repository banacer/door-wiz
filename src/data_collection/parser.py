import argparse
from serial import Serial
from time import time
from eventdetector import EventDetector
from Pubsub import pub
import json
'''
This module runs on Raspberry PI. It reads from the serial the sensor data that are transformed to distance, calibrated.
If also detects a walking event and passes the event to the next node
'''

def run(port, max_height, max_width, calibration, door):
    ser = Serial(port, 9600)
    prev = time()
    detector = EventDetector(130,200,4, door)
    while True:
        try:
            line = ser.readline().rstrip('\n\r')
            data = line.split(',')

            if len(data) not in [3,4]: # sometimes temperature is sent which makes it 4
                continue
            for i in range(3):
                try:
                    data[i] = calibration * float(data[i])
                except ValueError:
                    continue
            now = time()
            if len(data) ==  4: # we will push temperature to rabbitmq
                try:
                    temp_dict = {'temp': float(data[3]), 'time': now}
                    pub('temperature',json.dumps(temp_dict))
                except ValueError as e:
                    print e
            rate = 1 / (now - prev)
            ut = data[0]
            ul = data[1]
            ur = data[2]
            width = 0
            height = max_height - ut
            if not (ul > 120 and ur > 120):
                width = max_width - ul - ur
            detector.get_reading(height, width, rate, ut, ul, ur)
            #print '{:5.2f} {:5.2f} {:5.2f} {:5.2f} {:4.2f}'.format(height, ul, ur, width, rate)
            prev = now
        except Exception as e:
            print e

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--rabbitip', help="The IP address of RabbitMQ server", type=str, default='172.26.56.122')
    parser.add_argument('-p', '--rabbitport', help="The PORT of RabbitMQ server", type=int, default=5672)
    parser.add_argument('-x','--exchange',help='The exchange name of RabbitMQ server')
    args = parser.parse_args()
    door = args.exchange
    print 'door', door
    calibration = .01877037
    max_height = 223
    max_width = 123
    run(port='/dev/ttyACM0', max_height=max_height, max_width=max_width, calibration=calibration, door=door)
