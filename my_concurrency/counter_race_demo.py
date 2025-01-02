import threading

global_num = 0

def add_repeat(count):
    global global_num
    for _ in range(count):
        global_num += 1


count = 1000_000
threads_count = 2
threads = []

for _ in range(threads_count):
    t = threading.Thread(target=add_repeat, args=(count,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()


print(f'expect {threads_count * count}, got {global_num}')