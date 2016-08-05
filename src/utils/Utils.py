"""
This file contains a set of utilities function needed by other modules
"""
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pymongo import MongoClient

import pika
import sys


def convert_file_to_data_frame(filename, id, MAX_HEIGHT, MAX_WIDTH):
    """
    read data from file in the format:
    UL=<>
    UR=<>
    UT=<>
    :param filename: the path to the file
    :param id: the identifier of the person generating the data
    :return: frame with height, width
    """
    my_file = open(filename, 'r')
    lines = my_file.readlines()
    dict = {}
    data = []
    for line in lines:
        key = line.split('=')[0].rstrip()
        val = line.split('=')[1].rstrip()
        if dict.has_key(key):
            # we probably have all of them at this point
            height = MAX_HEIGHT - dict['UT']
            if height < 5:
                height = np.nan
            width = np.nan
            if dict.has_key('UL') and dict.has_key('UR'):
                if dict['UL'] > 140 or dict['UR'] > 140:
                    width = np.nan
                else:
                    width = MAX_WIDTH - dict['UL'] - dict['UR']
            data.append([height, width])
            dict = {}
        else:
            dict[key] = float(val)
    frame = DataFrame(data, columns=['height', 'width'])
    frame['id'] = id
    return frame


def get_frame(path):
    result = []
    for id in range(1, 21):
        filename = path + 'u%d.dat' % id
        frame = convert_file_to_data_frame(filename, id)
        result.append(frame)
    frame = pd.concat(result, ignore_index=True)
    return frame


def printit(ch, method, properties, body):
    """
    prints the body message. It's the default callback method
    :param ch: keep null
    :param method: keep null
    :param properties: keep null
    :param body: the message
    :return:
    """
    print(" [x] %r" % body)


def sub(queue_name, callback=printit, host='172.26.50.120'):
    """
    Connects to queue
    :param queue_name: the queue to subscribe to
    :param callback: optional callback function
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def pub(queue_name, message, host='172.26.50.120'):
    """
    publish to queue
    :param queue_name: queue name
    :param message: message
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    # channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print" [x] Sent %s" % message
    connection.close()


def init_mongo_client( mongo_ip, mongo_port):
    '''
    returns client connection to mongodb "local" database
    :param mongo_ip: mongodb ip address
    :param mongo_port:mongodb port
    :return: database connection object
    '''
    client = MongoClient(mongo_ip, mongo_port)
    db = client.local
    return db
