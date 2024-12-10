# Test for class view
import view
import threading
import time

sum: int = 0
threads = []
n_threads: int = 1000
x: int = 1000

lock = threading.Lock()

def print_thread(number: int):
    #lock.acquire()
    global sum
    print({threading.current_thread().name})
    for i in range(x):
        lock.acquire()
        y = sum
        time.sleep(0.0001)
        sum = y + 1
        lock.release()
    #lock.release()

if __name__=='__main__':
    for i in range(n_threads):
        threads.append(threading.Thread(target=print_thread, args=(i,), name=f"Thread {i}"))
        threads[i].start()
    for t in threads:
        t.join()
    print(f"Soma certa: {n_threads*x:>12}")
    print(f"Soma: {sum:>18}")