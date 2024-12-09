import time
from collections import deque
import heapq

class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = []
        self.task = None

    def add_task(self, task):
        self.ready.append(task)
    
    def sleep(self, delay):
        ttl = time.time() + delay
        heapq.heappush(self.sleeping, (ttl, self.task))
        self.task = None

    def run(self):
        while self.ready or self.sleeping:
            if self.ready:
                self.task = self.ready.popleft()
                try:
                    next(self.task)
                    if self.task: # TODO: why we need this check
                        self.ready.append(self.task)
                except StopIteration:
                    pass
            else:
                ttl, task = heapq.heappop(self.sleeping)
                delay = ttl - time.time()
                if delay > 0:
                    time.sleep(delay)
                self.ready.append(task)
    
def countdown(n):
    while n > 0:
        print("Down: ", n)
        sched.sleep(.4)
        yield
        n -= 1


def countup(stop):
    n = 0
    while n < stop:
        print("Up: ", n)
        sched.sleep(.1)
        yield
        n+=1
    

sched = Scheduler()
sched.add_task(countdown(5))
sched.add_task(countup(20))
sched.run()
