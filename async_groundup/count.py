import time
import threading



def countdown(n):
    while n > 0:
        print("Down: ", n)
        time.sleep(1)
        n -= 1


def countup(stop):
    n = 0
    while n < stop:
        print("Up: ", n)
        time.sleep(1)
        n+=1
    

threading.Thread(target=countdown, args=(5,)).start()
threading.Thread(target=countup, args=(5,)).start()