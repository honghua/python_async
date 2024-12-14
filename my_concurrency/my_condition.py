from collections import deque
from threading import Lock

class Condition:
    def __init__(self, lock: Lock):
        self.lock = lock
        self.waiting_threads = deque()

    
    def wait(self):
        thread_lock = Lock()
        thread_lock.acquire()
        self.waiting_threads.append(thread_lock)

        self.lock.release()

        try:
            thread_lock.acquire() # waiting
        finally:
            self.lock.acquire()
    
    def notify(self):
        if self.waiting_threads:
            thread_lock = self.waiting_threads.popleft()
            thread_lock.release()