#!/usr/bin/python3

import json
import argparse
from multiprocessing.connection import Listener
from rf_transmitter import Transmitter

def parseArgs():
    parser = argparse.ArgumentParser(description='RF Server.')
    parser.add_argument('config', help='service configuration file')
    parser.add_argument('-p', '--port', type=int, default=8486, required=False,
                        help='server listen on port')
    return parser.parse_args()

def loadConfig(config_file):
    with open(config_file) as f:
        config = json.load(f)
    config['pin'] = int(config['pin'])
    return config

def requestHandler(conn, transmitter):
    msg = conn.recv()
    print('processing request {}...'.format(msg))
    try:
        if msg == ['exit']:
            conn.send("Terminating RF server...")
            return False

        if msg[0] == 'list':
            conn.send(transmitter.listRemotes(msg[1] if len(msg) > 1 else None))
            return True

        if len(msg) != 2:
            conn.send("Please provide remote and key name")
            return True

        if not transmitter.valid(msg[0], msg[1]):
            conn.send("'{} - {}' is not a valid key combination\n".format(msg[0], msg[1]) + transmitter.listRemotes(msg[0]))
            return True

        # send rf code
        transmitter.send(msg[0], msg[1])
        conn.send("Key '{}' on remote '{}' has been pressed".format(msg[1], msg[0]))
    except Exception as e:
        print("Following exception happenned while processing: {}".format(e))
    return True

def runServer(config_file, port):
    config = loadConfig(config_file)
    transmitter = Transmitter(config['pin'], config['remotesConfig'])

    address = ('localhost', port)
    with Listener(address) as listener:
        print('rfserver is listening at', address)
        while True:
            with listener.accept() as conn:
                print('connection accepted from', listener.last_accepted)
                if not requestHandler(conn, transmitter):
                    break

if __name__ == "__main__":
    args = parseArgs()
    runServer(args.config, args.port)
