from collections import deque
import time
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
    

sched = Scheduler()

class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()

    def put(self, item):
        self.items.append(item)
        if self.waiting:
            sched.add_task(self.waiting.popleft())
    
    def get(self):
        if not self.items:
            self.waiting.append(sched.task)
            sched.task = None
            yield
        return self.items.popleft()


q = AsyncQueue()

def producer(q, stop):
    i = 0
    while i < stop:
        q.put(i)
        print("producing: ", i)
        sched.sleep(.2)
        yield
        i+=1
    q.put(None)
    print("Producer finished!")


def consumer(q, name=""):
    while True:
        item = yield from q.get() # blocking
        if item is None:
            break
        print(f"{name} consuming: ", item)
    print(f"{name} Consumer finished")
    

sched.add_task(producer(q, 10))
sched.add_task(consumer(q, "lena"))
sched.add_task(consumer(q, "harry"))
sched.run()
