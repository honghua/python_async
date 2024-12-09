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
                    if self.task: # TODO: explain why we need this check
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

class QueueClosed(Exception):
    pass

class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()
        self.closed = False

    def put(self, item):
        if self.closed:
            raise QueueClosed
        self.items.append(item)
        if self.waiting:
            sched.add_task(self.waiting.popleft())
    
    def get(self):
        # if not self.items:
        while not self.items: #TODO(): explain why while loop is needed
            if self.closed:
                raise QueueClosed
            self.waiting.append(sched.task)
            sched.task = None
            yield
        return self.items.popleft()

    def close(self):
        self.closed = True
        while self.waiting:
            sched.add_task(self.waiting.popleft())

q = AsyncQueue()

def producer(q: AsyncQueue, stop):
    i = 0
    while i < stop:
        q.put(i)
        print("producing: ", i)
        sched.sleep(.2)
        yield
        i+=1
    q.close()
    print("Producer finished!")


def consumer(q, name=""):
    while True:
        try:
            item = yield from q.get() # blocking
            print(f"{name} consuming: ", item)
        except QueueClosed:
            break
    print(f"{name} Consumer finished")
    

sched.add_task(producer(q, 10))
sched.add_task(consumer(q, "A"))
# sched.add_task(consumer(q, "B"))
sched.run()
