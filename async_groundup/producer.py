from queue import Queue
from collections import deque

import time
import threading



q = Queue()

def producer(q, stop):
    i = 0
    while i < stop:
        q.put(i)
        print("producing: ", i)
        time.sleep(.2)
        i+=1
    q.put(None)
    print("Producer finished!")


def consumer(q):
    while True:
        item = q.get() # blocking
        if item is None:
            break
        print("consuming: ", item)
    print("Consumer finished")
    

threading.Thread(target=producer, args=(q, 10,)).start()
threading.Thread(target=consumer, args=(q,)).start()
