#!/usr/bin/python

import sys
import time
import json
import RPi.GPIO as GPIO

def transmit(codes, pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    s = True
    for t in codes:
        GPIO.output(pin, int(s))
        time.sleep(t/1000000.)
        s = not s

    GPIO.output(pin, 0)
    GPIO.cleanup()

def readSignalFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    signal = [line.strip().split('\t') for line in lines]
    return [(int(s[0]), int(s[1])) for s in signal]

def logConfig(config):
    with open(config) as f:
        remotes = json.load(f)
    for remote in remotes.values():
        for key in remote:
            remote[key] = list(map(int, remote[key].split()))
    return remotes

if __name__ == "__main__":
    remotes = logConfig(sys.argv[1])
    transmitter_pin = int(sys.argv[2])
    print("Load {} remotes: {}".format(len(remotes), ' '.join(remotes.keys())))
    print("Transmitting on pin {}".format(transmitter_pin))

    while True:
        command = raw_input('Input remote and key (EXIT to stop) --> ')
        if command == 'EXIT':
            break
        remote, key = command.split()
        code = remotes[remote][key]
        transmit(code, transmitter_pin)
