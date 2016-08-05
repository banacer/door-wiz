import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import pymongo
from pymongo import MongoClient
from Pubsub import pub, sub
from src.ml import Features as extractor
from src.utils import Utils

class EventProcessor(object):
    def __init__(self, mongo_ip, mongo_port, collection_name):
        self.db = Utils.init_mongo_client(mongo_ip, mongo_port)
        self.collection_name = collection_name

    def save_to_db(self, walking_dict):
        print self.collection_name
        collection = self.db[self.collection_name]
        walk_id = collection.insert(walking_dict)
        return walk_id

    def extract_features(self, data):
        sampling_rate = 33
        default_speed = 5
        features = extractor.extract_all(data, sampling_rate, default_speed)
        return features

    def process_walking_event(self, ch, method, properties, body):
        walking_dict = json.loads(body)
        self.save_to_db(walking_dict)
        data = DataFrame(walking_dict)
        #data = self.clean_data(data)
        features = self.extract_features(data)
        print features

    @staticmethod
    def clean_data(data):
        data[data < 5] = np.nan
        data.dropna(how='all')
        data.interpolate(method='spline',order=5) # will have to see what order number is best. Just picked 4 by default
        return data

def run(mongo_ip, mongo_port, walking_raw):
        eventProcessor = EventProcessor(mongo_ip, mongo_port, walking_raw)
        sub('door', eventProcessor.process_walking_event)

if __name__ == '__main__':
    mongo_ip = '172.26.56.122'
    mongo_port = 27017
    walking_raw = 'walking_raw'
    run(mongo_ip, mongo_port, walking_raw)