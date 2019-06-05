import zmq
import time
import random
from threading import Thread


class StockManager(Thread):
    def __init__(self, metadata, generator, broker):
        Thread.__init__(self)
        self.stock_value = generator["initial_value"]
        self.generator = generator
        self.metadata = metadata
        self.dead = False
        self.socket = zmq.Context().socket(zmq.PUB)
        self.socket.connect("tcp://127.0.0.1:5559")

    def run(self):
        while True:
            if self.dead:
                break
            sleep_time = self.generator["min_wait"] + \
                (random.randint(0, 100)/100) * self.generator["max_wait"]
            time.sleep(sleep_time)
            deviation = (random.randint(-100, 100) /
                         100) * self.generator["max_deviation"]
            self.stock_value += deviation
            self.socket.send_string(
                self.metadata["name"]+" "+str(self.stock_value))
            print("Sending stock",
                  self.metadata["name"], "as ", self.stock_value)

    def stop(self):
        self.dead = True
