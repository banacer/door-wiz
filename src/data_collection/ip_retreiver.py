import Pubsub as p
import socket
import json
import argparse
import time

def run(name):
    d = {}
    d['name'] = name
    d['ip'] = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    print 'd is', d
    p.pub('rpi_ips',json.dumps(d))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help="RPI name", type=str,default='local')
    args = parser.parse_args()
    if args.name:
        name = args.name
        while True:
            run(name)
            time.sleep(300)