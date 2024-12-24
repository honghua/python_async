import threading
import time
import random

num = 0

def add_repeat(count):
    global num
    for _ in range(count):
        time.sleep(random.uniform(0, 0.000001))
        num += 1


print(num)
count = 1000_000
t1 = threading.Thread(target=add_repeat, args=(count,))
t1.start()

t2 = threading.Thread(target=add_repeat, args=(count,))
t2.start()

t1.join()
t2.join()
print(num)