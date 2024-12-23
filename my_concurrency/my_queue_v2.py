from collections import deque
import queue
import time
import threading

# -------------------------------
import my_condition

#   c c c       L     dining area [  i  ]
#               p
#                      waiting area [ c c  ]
  
class Queue:
    def __init__(self):
        self.lock = threading.Lock()
        self.items = deque()
        self.not_empty = my_condition.Condition(self.lock)
    
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
q = Queue()
threading.Thread(target=producer, args=(q, 10)).start()
threading.Thread(target=consumer, args=(q, "A")).start()
threading.Thread(target=consumer, args=(q, "B")).start()
