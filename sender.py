#!/usr/bin/python

import sys
import time
import RPi.GPIO as GPIO

def transmit(codes, pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    for s, t in codes:
        GPIO.output(pin, s)
        time.sleep(t/1000000.)

    GPIO.output(pin, 0)
    GPIO.cleanup()

def readSignalFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    signal = [line.strip().split('\t') for line in lines]
    return [(int(s[0]), int(s[1])) for s in signal]

if __name__ == "__main__":
    signal_file = sys.argv[1]
    transmitter_pin = int(sys.argv[2])
    transmit(readSignalFile(signal_file), transmitter_pin)
