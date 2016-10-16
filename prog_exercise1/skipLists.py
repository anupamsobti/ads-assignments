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

        def updateSentinelHeight(self):
            prevSelf = self
            while self.level < math.log(self.noOfNodes,2):
                self = increaseHeight(self)
                self.noOfNodes = prevSelf.noOfNodes
            return self

        def increaseHeight(node):
            prevNode = node
            while prevNode.back != None:
                if prevNode.up != None:
                    prevNode = prevNode.up
                    break
                prevNode = prevNode.back

            if prevNode.back == None and prevNode.up != None:
                prevNode = prevNode.up

            if prevNode != node:
                #print("Found previous node",prevNode.data," Level = ",prevNode.level)
                newNode = listNode(node.data,front = prevNode.front,back = prevNode,up = None,down = node,level = node.level + 1)
                node.up = newNode
                if prevNode.front != None:
                    prevNode.front.back = newNode
                prevNode.front = newNode
                return newNode
            else:
                #print("Updating Sentinel")
                newNode = listNode(node.data,front = None,back = None,up = None,down = node,level = node.level + 1)
                node.up = newNode
                return newNode
                

        #print (self.search(x))
        isPresent,node = self.search(x)
        if not isPresent:
            self.noOfNodes += 1

            self = updateSentinelHeight(self)

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
                    #print("New Height for ",newNode.data," = ",newNode.level)
                else:
                    break

        return self

    def search(self,x):
        node = self
        if x == node.data:
            #while node.down != None:
            #    node = node.down
            #print("Found match at ",node.level)
            return True,node
        elif x > node.data:
            if node.front != None:
                return node.front.search(x)
            else:
                if node.down != None:
                    return node.down.search(x)
                else:
                #while node.down != None:
                #    node = node.down
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
        isPresent,node = self.search(x)
        if isPresent:
            #print("No of nodes = ",self.noOfNodes)
            self.noOfNodes -= 1
            if node.back == None:
                print("Never expected this")
            while node != None:
                node.back.front = node.front
                node.front.back = node.back
                node = node.down
            
sentinel = -10000
myList = listNode(sentinel)
myList = myList.insert(4)
myList = myList.insert(5)
myList = myList.insert(1)

for i in range(1000):
    #myList = myList.insert(random.randrange(-999,1000))
    myList = myList.insert(i)

for i in range(200):
    #myList.delete(random.randrange(-999,1000))
    myList.delete(i)
#for i in range(10000):
#    myList = myList.insert(random.randrange(-9999,10000))

print("Search 5 result : ",myList.search(5))
print("Search 220 result : ",myList.search(220))
#myList.delete(5)
print("Level : ",myList.search(220)[1].level)
print(myList.level)
print(myList.noOfNodes)
