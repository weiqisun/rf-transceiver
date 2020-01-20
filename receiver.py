#!//usr/bin/python3

from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO
import sys

RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 5

if __name__ == '__main__':
    receive_pin = int(sys.argv[1])
    signal_file = sys.argv[2]
    print("recording signal from pin {} and will write to file '{}'...".format(receive_pin, signal_file))
    choice = input("Proceed? [Y/n]: ").strip().lower()
    print(choice)
    if choice and choice != 'y':
        print("Terminating process...")
        exit(0)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(receive_pin, GPIO.IN)
    cumulative_time = 0
    beginning_time = datetime.now()
    print('**Started recording**')
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(receive_pin))
        cumulative_time = time_delta.seconds
    print('**Ended recording**')
    print(len(RECEIVED_SIGNAL[0]), 'samples recorded')
    GPIO.cleanup()

    with open(signal_file, 'w') as f:
        for t, s in zip(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1]):
            f.write('{}\t{}\n'.format(t, s))

    print('**Processing results**')
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    print('**Plotting results**')
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.show()
