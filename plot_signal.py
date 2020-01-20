#!/usr/bin/python3

import re
import sys
from datetime import timedelta
import matplotlib.pyplot as pyplot
from receiver import MAX_DURATION

regex = re.compile(r'((?P<hours>\d+):)((?P<minutes>\d+):)((?P<seconds>\d+))(\.(?P<microseconds>\d+))?')

def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

if __name__ == "__main__":
    signal_file = sys.argv[1]
    duration = []
    signal = []
    with open(signal_file) as f:
        for line in f:
            print(line.strip())
            tokens = line.strip().split("\t")
            duration.append(parse_time(tokens[0]).total_seconds())
            signal.append(int(tokens[1]))

    print('**Plotting results**')
    pyplot.plot(duration, signal)
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
