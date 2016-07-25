import pika
import logging
import sys
import json
import pandas as pd

__host = '172.26.56.122'
__port = 5672
logger = logging.getLogger()

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

def print_sensor_data(ch, method, properties, body):
    """
    prints the body message. It's the default callback method
    :param ch: keep null
    :param method: keep null
    :param properties: keep null
    :param body: the message
    :return:
    """
    data = json.load(body)
    print data["UT"], data["UL"], data["UR"]

def print_distance_data(ch, method, properties, body):
    """
    prints the body message. It's the default callback method
    :param ch: keep null
    :param method: keep null
    :param properties: keep null
    :param body: the message
    :return:
    """
    calibration_a = 0.013696
    calibration_b = -3.56201
    data = json.loads(body)
    data['UT'] = calibration_a * float(data['UT']) + calibration_b
    data['UL'] = calibration_a * float(data['UL']) + calibration_b
    data['UR'] = calibration_a * float(data['UR']) + calibration_b
    print data["UT"], data["UL"], data["UR"]

def sub(exchange_name,callback=printit):
    """
    Connects to queue
    :param exchange_name: the exchange to subscribe to
    :param callback: optional callback function
    :return:
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=__host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, type='fanout')
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    print(' [*] Waiting for logs. To exit press CTRL+C')
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()



def pub(exchange_name, message):
    """
    publish to queue
    :param exchange_name: queue name
    :param message: message
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=__host))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, type='fanout')
    channel.basic_publish(exchange=exchange_name, routing_key='', body=message)
    logger.info('Message sent: {0}'.format(message))
    connection.close()