#!/usr/bin/python3
import sys
import math
import random

class listNode():
    def __init__(self,data,front=None,back=None,up=None,down=None,level=0):
        self.data = data
        self.front = front
        self.back  = back
        self.up = up
        self.down = down
        self.level = level
        self.noOfNodes = 1

    def insert(self,x):

        def tossACoin():
            return bool(random.getrandbits(1))

        def updateSentinelHeight(self,newNode):
            while self.level < newNode.level:
                self = increaseHeight(self)
            return self

        def increaseHeight(node):
            prevNode = node
            while prevNode.back != None:
                if prevNode.up != None:
                    prevNode = prevNode.up
                    break
                prevNode = prevNode.back
            if prevNode != node:
                return listNode(node.data,front = prevNode.front,back = prevNode,up = None,down = node,level = node.level + 1)
            else:
                return listNode(node.data,front = node.front,back = None,up = None,down = None,level = node.level + 1)

        #print (self.search(x))
        isPresent,node = self.search(x)
        if not isPresent:
            self.noOfNodes += 1
            if x > node.data:
                newNode = listNode(x,front = node.front,back = node)
                node.front = newNode
                if newNode.front != None:
                    newNode.front.back = newNode
            else:   #x < node.data
                newNode = listNode(x,front = node,back = node.back)
                node.back = newNode
                if newNode.back != None:
                    newNode.back.front = newNode


            while newNode.level < math.log(self.noOfNodes,2):
                if tossACoin():
                    newNode = increaseHeight(newNode)
                else:
                    break

            return updateSentinelHeight(self,newNode)
        return self

    def search(self,x):
        node = self
        if x == node.data:
            #while node.down != None:
            #    node = node.down
            return True,node
        elif x > node.data:
            if node.front != None:
                return node.front.search(x)
            else:
                while node.down != None:
                    node = node.down
                return False,node
        else: #if x < node.data:
            if node.back != None:
                if node.level == 0:
                    return False,node
                else:
                    return node.back.down.search(x)
            else:
                while node.down != None:
                    node = node.down
                return False,node

    def delete(self,x):
        pass

sentinel = -10000
myList = listNode(sentinel)
myList = myList.insert(4)
myList = myList.insert(5)
myList = myList.insert(1)

for i in range(1000):
    myList = myList.insert(random.randrange(-1000,1000))

print(myList.search(5))
