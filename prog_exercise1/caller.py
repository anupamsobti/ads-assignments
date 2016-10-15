#!/usr/bin/python3
import sys
import threading

def runSkipList():
    import skipLists

threading.stack_size(67108864) # 64MB stack
sys.setrecursionlimit(2 ** 20) # something real big
                               # you actually hit the 64MB limit first
                               # going by other answers, could just use 2**32-1

# only new threads get the redefined stack size
thread = threading.Thread(target=runSkipList)
thread.start()

