from collections import deque
import queue
import time
import threading

# --------------------------------
class Condition:
    def __init__(self, lock):
        self.waiters = deque()
        self.lock = lock

    def wait(self):
        waiter = threading.Lock()
        waiter.acquire()
        self.waiters.append(waiter)
        
        self.lock.release()

        waiter.acquire()  # acquire lock 2nd time makes os waiting for the current thread!!!
        self.lock.acquire()
        waiter.release()
        
        
        
    def notify(self):
        if self.waiters:
            waiter = self.waiters.popleft()
            waiter.release()

#   c c c       L     dining area [  i  ]
#               p
#                      waiting area [ c c  ]
  
class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.items = deque()
        self.not_empty = Condition(self.lock)
    
    def get(self): # how to block on get???
        with self.lock:
            while not self.items:
                self.not_empty.wait()
            return self.items.popleft()
    
    def put(self, item):
        with self.lock:
            self.items.append(item)
            self.not_empty.notify()
        
            

# ----


def producer(q, count):
    for i in range(count):
        q.put(i)
        print("producing: ", i)
        time.sleep(.2)

def consumer(q, name=""):
    while True:
        # time.sleep(.1)
        print(f"{name} conusming: ", q.get())




# q = queue.Queue() # blocking queue
q = Queue()         # non-blocking queue
threading.Thread(target=producer, args=(q, 10)).start()
threading.Thread(target=consumer, args=(q, "A")).start()
threading.Thread(target=consumer, args=(q, "B")).start()
