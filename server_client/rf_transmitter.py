import time
import json
import RPi.GPIO as GPIO

def loadRemotes(config):
    with open(config) as f:
        remotes = json.load(f)
    for remote in remotes.values():
        for key in remote:
            signal = True
            code = []
            for timing in remote[key].split():
                code.append((int(signal), int(timing)/1000000.))
                signal = not signal
            remote[key] = code
    return remotes

class Transmitter:
    def __init__(self, pin, remotes_config):
        self.pin = pin
        self.remotes = dict()
        for config in remotes_config:
            self.remotes.update(loadRemotes(config))

        # setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

    def send(self, remote, key):
        code = self.remotes[remote][key]
        signal = True
        for signal, timing in code:
            GPIO.output(self.pin, signal)
            time.sleep(timing)
        GPIO.output(self.pin, 0)

    def listAllRemotes(self):
        res = "Following remotes are avialable:"
        for remote in self.remotes:
            res += "\n  {}".format(remote)
        return res

    def listAllRemoteKeys(self, remote):
        res = "Following keys are avialable in {}:".format(remote)
        for key in self.remotes[remote]:
            res += "\n  {}".format(key)
        return res

    def listRemotes(self, remote=None):
        if not remote:
            return self.listAllRemotes()
        if remote and remote not in self.remotes:
            return "'{}' is not a valid remote\n".format(remote) + self.listAllRemotes()
        return self.listAllRemoteKeys(remote)

    def valid(self, remote, key):
        return remote and remote in self.remotes and key and key in self.remotes[remote]

    def __del__(self):
        GPIO.cleanup()
