import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-rip', '--rabbitip', help="The IP address of RabbitMQ server", type=str)
    parser.add_argument('-rp', '--rabbitport', help="The PORT of RabbitMQ server", type=int)
    args = parser.parse_args()
    print args.square ** 2
