# -*- coding: utf-8 -*-
import sys
import tornado.ioloop
import tornado.web
import sockjs.tornado
import pika
from pika import adapters
import datetime
import json


class BrokerConnection(sockjs.tornado.SockJSConnection):
    clients = set()

    def on_open(self, info):
        logging.info('Incoming client from %s' % info.ip)
        self.clients.add(self)
        self.health_exchange = 'rpi_ips'
        self.walk_exchange = 'door'
        self.host = '172.26.56.122'
        logging.debug('Events: Connecting to RabbitMQ:')
        self.connection = pika.TornadoConnection(pika.ConnectionParameters(host=self.host),
                                                 on_open_callback=self.on_connected)

    def on_connected(self, unused_connection):
        logging.debug("Events: Opening a channel")
        self.channel = self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel.exchange_declare(exchange=self.health_exchange, type='fanout')
        result = self.channel.queue_declare(self.on_hdeclareok, exclusive=True)

        self.channel.exchange_declare(exchange=self.walk_exchange, type='fanout')
        result = self.channel.queue_declare(self.on_wdeclareok, exclusive=True)
        # We should be connected if we made it this far
        self.connected = True

    def on_hdeclareok(self, result):
        self.health_queue = result.method.queue
        self.channel.queue_bind(self.on_hbindok, exchange=self.health_exchange, queue=self.health_queue)

    def on_wdeclareok(self, result):
        self.walk_queue = result.method.queue
        self.channel.queue_bind(self.on_wbindok, exchange=self.walk_exchange, queue=self.walk_queue)

    def on_hbindok(self, frame):
        self.channel.basic_consume(self.on_health, queue=self.health_queue, no_ack=True)

    def on_wbindok(self, frame):
        self.channel.basic_consume(self.on_walk, queue=self.walk_queue, no_ack=True)

    def on_message(self, message):
        logging.debug('Received something from client: %s', message)

    def on_close(self):
        self.clients.remove(self)

    def on_health(self, unused_channel, basic_deliver, properties, body):
        for c in self.clients:
            msg_received = json.loads(body)
            msg_received['type'] = msg_received['name']+'_h'
            msg_received['data'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg_to_send = json.dumps(msg_received)
            print 'sending', msg_to_send
            c.send(msg_to_send)

    def on_walk(self, unused_channel, basic_deliver, properties, body):
        for c in self.clients:
            msg_received = json.loads(body)
            msg_received['type'] = 'walk'
            msg_to_send = json.dumps(msg_received)
            c.send(msg_to_send)


if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.INFO)

    BrokerRouter = sockjs.tornado.SockJSRouter(BrokerConnection, '/push')

    app = tornado.web.Application(BrokerRouter.urls)
    port = 9091
    app.listen(port)
    print('Listening on port %d for queue %s', port, 'hello')
    tornado.ioloop.IOLoop.instance().start()
