import numpy as np
import pandas as pd
import Pubsub as p
from json import dumps
class EventDetector(object):

    def __init__(self, min_height, max_height,max_consecutive_errors):
        self.walk = {'height':[], 'width':[]}
        self.min_height = min_height
        self.max_height =max_height
        self.max_consecutive_errors = max_consecutive_errors
        self.current_errors = 0
        self.is_start = False

    def get_reading(self, height, width):
        if height > self.min_height and height < self.max_height:
            self.current_errors = 0
            if not self.is_start:
                self.is_start = True
            self.walk['height'].append(height)
            self.walk['width'].append(width)
        else:
            if self.is_start and self.current_errors < self.max_consecutive_errors:
                self.walk['height'].append(height)
                self.walk['width'].append(width)
                self.current_errors += 1
            elif self.is_start:
                self.finalize_walking_event()

    def finalize_walking_event(self):
        self.current_errors = 0
        self.is_start = False
        print 'sending frame!'
        p.pub('door', dumps(self.walk))
        self.walk['height'] = []
        self.walk['width'] = []