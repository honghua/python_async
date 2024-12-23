from collections import deque
from threading import Lock

class Condition:
    def __init__(self, lock):
        self.waiters = deque()
        self.lock = lock

    def wait(self):
        waiter = Lock()
        waiter.acquire()
        self.waiters.append(waiter)
        
        self.lock.release()

        try:
            waiter.acquire()  # acquire lock 2nd time makes os waiting for the current thread!!!
        finally:
            self.lock.acquire()
        
        
    def notify(self):
        if self.waiters:
            waiter = self.waiters.popleft()
            waiter.release()