#!/usr/bin/python

import sys

def timeToInt(time_str):
    return int(round(float(time_str.lstrip("0:")) * 1000000))

def decode(signals, onset=0, offset=float("inf")):
    codes = []
    pre_signal = 0
    pre_timing = 0
    current_duration = 0

    for t, s in signals:
        timing = timeToInt(t)
        signal = int(s)
        if timing < onset:
            continue
        if timing > offset:
            break

        current_duration += timing - pre_timing
        if signal != pre_signal:
            codes.append((pre_signal, current_duration))
            current_duration = 0
        pre_signal = signal
        pre_timing = timing

    if current_duration:
        codes.append((pre_signal, current_duration))

    if not codes[-1][0]:
        codes = codes[:-1]
    if not codes[0][0]:
        codes = codes[1:]
    return codes

def readRawSignal(filename):
    with open(filename) as f:
        lines = f.readlines()
    return [line.strip().split('\t') for line in lines]

def writeSignal(filename, codes):
    with open(filename, 'w') as f:
        for s, t in codes:
            f.write('{}\t{}\n'.format(s, t))

if __name__ == "__main__":
    raw_signal_file = sys.argv[1]
    outfile = sys.argv[2]
    start = int(float(sys.argv[3]) * 1000000)
    end = int(float(sys.argv[4]) * 1000000)
    writeSignal(outfile, decode(readRawSignal(raw_signal_file), start, end))
