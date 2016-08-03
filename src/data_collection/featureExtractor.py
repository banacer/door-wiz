import pandas as pd
from pandas import DataFrame, Series
import pymongo
from pymongo import MongoClient
from src.ml import Features as extractor

class FeatureExtractor(object):
    def __init__(self, mongo_ip, mongo_port):
        self.db = FeatureExtractor.init_mongo_client()

    def save_to_db(self, db, collection_name, walking_dict):
        collection = db[collection_name]
        walk_id = collection.insert(walking_dict)
        return  walk_id

    def extract_features(self, db, collection_name='walking_features',walking_dict = {}):
        data = DataFrame(walking_dict)
        features = extractor.extract_all(data)
        save_to_db(db, collection_name, collection_name, features)

    def get_walking_event(ch, method, properties, body):
        pass
    def run():
