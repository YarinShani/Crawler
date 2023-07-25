import threading
from multiprocessing import Queue


class Manager(object):
    def __init__(self):
        self.queue = Queue()
        self.size = 0
        self.lock = threading.Lock()

    def put(self, element):
        self.queue.put(element)
        self.size += 1

    def get(self):
        self.lock.acquire()

        if self.size < 1:
            self.lock.release()
            return None

        self.size -= 1
        response = self.queue.get()

        self.lock.release()

        return response

    def qsize(self):
        return self.size

    def empty(self):
        return self.size == 0
