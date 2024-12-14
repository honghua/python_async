import heapq
import time
from collections import deque

class Awaitable:
    def __await__(self):
        yield

def switch():
    return Awaitable()

class Scheduler:
    def __init__(self) -> None:
        self.ready = deque()
        self.sleeping = []
        self.task = None

    def add_task(self, task):
        self.ready.append(task)
    
    def run(self):
        while self.ready or self.sleeping:
            if self.ready:
                self.task = self.ready.popleft()
                try:
                    # next(self.task)
                    self.task.send(None)
                    if self.task:
                        self.ready.append(self.task)
                except StopIteration:
                    pass
            else:
                ttl, task = heapq.heappop(self.sleeping)
                delay = ttl - time.time()
                if delay > 0:
                    time.sleep(delay)
                self.add_task(task)

    async def sleep(self, delay):
        ttl = time.time() + delay
        heapq.heappush(self.sleeping, (ttl, self.task))
        self.task = None
        await switch()


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
        
    async def get(self):
        while not self.items:
            if self.closed:
                raise QueueClosed
            self.waiting.append(sched.task)
            sched.task = None
            await switch()
        return self.items.popleft()
    
    def close(self):
        self.closed = True
        while self.waiting:
            sched.add_task(self.waiting.popleft())


async def producer(q, stop):
    i = 0
    while i < stop:
        q.put(i)
        print("producing: ", i)
        await sched.sleep(.2)
        i+=1
    # q.put(None)
    q.close()
    print("Producer finished!")


async def consumer(q):
    while True:
        try:
            item = await q.get() # blocking
            print("consuming: ", item)
        except QueueClosed:
            break
    print("Consumer finished")
    

q = AsyncQueue()
sched.add_task(producer(q, 5))
sched.add_task(consumer(q))
sched.add_task(consumer(q))
sched.run()


