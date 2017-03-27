import numpy as np
import Pubsub as p
from json import dumps
from time import time
class EventDetector(object):

    def __init__(self, min_height, max_height,max_consecutive_errors, door):
        self.walk = {'height':[], 'width':[]}
        self.data = {'ut':[], 'ul':[], 'ur':[]}
        self.min_height = min_height
        self.max_height =max_height
        self.max_consecutive_errors = max_consecutive_errors
        self.current_errors = 0
        self.is_start = False
        self.sum_sampling_rate = 0
        self.door = door
        self.exchange = 'door'

    def get_reading(self, height, width, sampling_rate, ut, ul, ur):
        if height > self.min_height and height < self.max_height:
            self.current_errors = 0
            if not self.is_start:
                self.is_start = True
            self.walk['height'].append(height)
            self.walk['width'].append(width)
            self.data['ut'].append(ut)
            self.data['ul'].append(ul)
            self.data['ur'].append(ur)
            self.sum_sampling_rate += sampling_rate
        else:
            if self.is_start and self.current_errors < self.max_consecutive_errors:
                self.walk['height'].append(height)
                self.walk['width'].append(width)
                self.data['ut'].append(ut)
                self.data['ul'].append(ul)
                self.data['ur'].append(ur)
                self.sum_sampling_rate += sampling_rate
                self.current_errors += 1
            elif self.is_start:
                self.finalize_walking_event()

    def finalize_walking_event(self):
        self.current_errors = 0
        self.is_start = False
        #print 'sending frame!'
        data = {}
        data['door'] = self.door
        data['time'] = time()
        data['sampling_rate'] = self.sum_sampling_rate / len(self.walk.keys())
        data['walk'] = self.walk
        data['raw'] = self.data
        p.pub(self.exchange, dumps(data))
        self.walk['height'] = []
        self.walk['width'] = []
        self.data['ut'] = []
        self.data['ul'] = []
        self.data['ur'] = []
        self.sum_sampling_rate = 0