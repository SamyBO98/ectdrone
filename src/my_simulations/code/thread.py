from multiprocessing import Process
import time

def func1(message):
    while True:
        print(message)


if __name__ == '__main__':
    first = Process(target=func1, args=("First Call",)).start()
    second = Process(target=func1, args=("Second Call",)).start()