#!/usr/bin/python3
import sys
import threading

def runSkipList():
    import skipLists

def runTwoThreeTrees():
    import two_three_Trees

def runRbTrees():
    import rb_trees

def runAVLTrees():
    import avlTrees

threading.stack_size(67108864) # 64MB stack
sys.setrecursionlimit(2 ** 20) # something real big
                               # you actually hit the 64MB limit first
                               # going by other answers, could just use 2**32-1

# only new threads get the redefined stack size
if sys.argv[-1] == "1":
    thread = threading.Thread(target=runTwoThreeTrees)
elif sys.argv[-1] == "2":
    thread = threading.Thread(target=runRbTrees)
elif sys.argv[-1] == "3":
    thread = threading.Thread(target=runAVLTrees)
elif sys.argv[-1] == "4":
    thread = threading.Thread(target=runSkipList)
else:
    print("invalid tree specified")
thread.start()

