from collections import deque
import queue
import time
import threading

# --------------------------------
class QueueFull(Exception):
    pass

class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.items = deque()
    
    def get(self): # how to block on get???
        with self.lock:
            if self.items:
                return self.items.popleft()
        return None
        
    def put(self, item):
        with self.lock:
            self.items.append(item)
        
            

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
