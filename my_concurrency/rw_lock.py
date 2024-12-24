import threading

class RWLock_r:
    '''
    RW lock favor reader
    '''
    def __init__(self):
        self.read_lock = threading.Lock()
        self.readers = 0
        self.write_lock = threading.Lock()
        
    def read_acquire(self):
        with self.read_lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire()
        
    def read_release(self):
        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()
    
    def write_acquire(self):
        self.write_lock.acquire()
    
    def write_release(self):
        self.write_lock.release()

class RWLock_w:
    '''
    RW lock favor writer
    '''
    def __init__(self):
        self.readers = 0

        self.write_lock = threading.Lock()
        self.condition = threading.Condition(self.write_lock)
        self.waiting_writers = 0
        self.active_writer = False
        
    def read_acquire(self):
        with self.write_lock:
            while self.active_writer or self.waiting_writers > 0:
                self.condition.wait()
            self.readers += 1
        
    def read_release(self):
        with self.write_lock:
            self.readers -= 1
            if self.readers == 0:
                self.condition.notify_all()
    
    def write_acquire(self):
        with self.write_lock:
            self.waiting_writers += 1
            while self.readers > 0 or self.active_writer:
                self.condition.wait()
            self.active_writer = True
    
    def write_release(self):
        with self.write_lock:
            self.active_writer = False
            self.condition.notifyAll()


def main():
    # writers: w
    
    # readers: r r r
    ...