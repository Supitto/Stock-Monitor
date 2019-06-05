from threading import Thread
import requests
import zmq


class Worker(Thread):
    def __init__(self, stock_name):
        Thread.__init__(self)
        self.listener_list = set()
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5560")
        # self.socket.setsockopt_string(zmq.SUBSCRIBE, stock_name)

    def add_listener(self, listener_url):
        self.listener_list.add(listener_url)

    def remove_listener(self, listener_url):
        self.listener_list.discard(listener_url)

    def run(self):
        while True:
            print("Listening")
            string = self.socket.recv()
            topic, messagedata = string.split()
            print(topic, messagedata)
