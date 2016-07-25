from serial import Serial
from time import time,sleep
import logging
from json import loads, dumps

import Pubsub as p

class Worker(object):
    __baudrate = 9600

    def __init__(self, port):
        self.ser = Serial(port, self.__baudrate)

    def run(self):
        #self.ser.flushInput()
        while True:
            line = self.ser.readline()
            logger.debug(line)
            data = line.split(',')
            logger.debug(data)
            if len(data) != 3:
                continue
            reading = {}
            reading['time'] = time()
            reading['UT'] = data[0]
            reading['UL'] = data[1]
            reading['UR'] = data[2]
            p.pub('d1',dumps(reading))

if __name__ == '__main__':
    w = Worker('/dev/ttyACM0')
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    w.run()