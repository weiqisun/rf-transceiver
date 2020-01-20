#!/usr/bin/python3

import json
import argparse
from multiprocessing.connection import Listener
from rf_transmitter import Transmitter

def parseArgs():
    parser = argparse.ArgumentParser(description='RF Server.')
    parser.add_argument('config', help='service configuration file')
    parser.add_argument('-p', '--port', type=int, default=8486, required=False,
                        help='service listen on port')
    return parser.parse_args()

def loadConfig(config_file):
    with open(config_file) as f:
        config = json.load(f)
    config['pin'] = int(config['pin'])
    return config

def runServer(config_file, port):
    config = loadConfig(config_file)
    transmitter = Transmitter(config['pin'], config['remotesConfig'])

    address = ('localhost', port)
    listener = Listener(address)
    print('rfserver is listening at', address)
    while True:
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        msg = conn.recv()
        print(msg)
        if msg == ['exit']:
            conn.close()
            break

        if msg[0] == 'list':
            transmitter.listRemotes(msg[1] if len(msg) > 1 else None)
            continue

        if len(msg) != 2:
            print("please provide remote and key name")
            continue

        # send rf code
        transmitter.send(msg[0], msg[1])

    listener.close()

if __name__ == "__main__":
    args = parseArgs()
    runServer(args.config, args.port)
