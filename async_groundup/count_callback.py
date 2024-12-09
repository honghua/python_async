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
        
        
sched = Scheduler()


def countdown(n):
    if n > 0:
        print("Down: ", n)
        sched.call_later(.4,lambda: countdown(n-1))


def countup(stop, n=0):
    if n < stop:
        print("Up: ", n)
        sched.call_later(.1, lambda: countup(stop, n+1))
    

sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(20))
sched.run()