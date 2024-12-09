import time
from collections import deque
import heapq


class Scheduler:
    def __init__(self) -> None:
        self.ready = deque()
        self.sleeping = [] # priorityqueue: sorted by excutation time

    def call_soon(self, callback):
        self.ready.append(callback)
        
    def call_later(self, delay, callback):
        ttl = delay + time.time()
        heapq.heappush(self.sleeping, (ttl, callback))
        
    def run(self):
        while self.ready or self.sleeping:
            if self.ready:
                func = self.ready.popleft()
                func()
            else:
                ttl, func = heapq.heappop(self.sleeping)
                delay = ttl - time.time()
                if delay > 0:
                    time.sleep(delay)
                self.call_soon(func)


class QueueClosed(Exception):
    pass

class Future:
    def __init__(self, value=None, exception=None):
        self.value = value
        self.exception = exception
        
    def result(self):
        if self.value:
            return self.value
        raise self.exception

class MyQueue:
    def __init__(self) -> None:
        self.items = deque()
        self.waiting = deque() # pending requests
        self.closed = False

    def put(self, item):
        if self.closed:
            raise QueueClosed
        self.items.append(item)
        if self.waiting:
            sched.call_soon(self.waiting.popleft())

    def get(self, callback): # blocking???
        if self.items:
            callback(Future(self.items.popleft()))
        elif self.closed:
            callback(Future(exception=QueueClosed))
        else:
            self.waiting.append(lambda: self.get(callback))
                
    
    def close(self):
        self.closed = True
        for func in self.waiting:
            sched.call_soon(func)
            

sched = Scheduler()
q = MyQueue()

def producer(q: MyQueue, stop):
    def _run(i):
        if i <= stop:
            q.put(i)
            print("producing: ", i)
            sched.call_later(0.1, lambda: _run(i+1)) # sleep for .1 second
        else:
            q.close()
            print("Producer finished!")
    _run(1)


def consumer(q, name:str=""):
    def _consume(future: Future):
        try:
            item = future.result()
            print(f"{name} consuming: ", item)
            sched.call_soon(lambda: consumer(q, name))
        except QueueClosed:
            print(f"{name} consumer Finished")
    q.get(_consume)
        
    

sched.call_soon(lambda: producer(q, 10))
sched.call_soon(lambda: consumer(q, "A"))
sched.call_soon(lambda: consumer(q, "B" ))
sched.call_soon(lambda: consumer(q, "C" ))
sched.run()


producer:  

consumer_queue: B C A
#  --- lambda exception demo

# def throw():
#     raise QueueClosed

# try:
#     lda = lambda: throw()
# except QueueClosed:
#     print("success")

# lda()


