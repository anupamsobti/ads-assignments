#!/usr/bin/python3

class rbTree():
    def __init__(self,data,color,parent=None,leftChild=None,rightChild=None,leaf=False):
        self.data = data
        self.color = color
        self.parent = parent
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.leaf = leaf

    def insertNode(self,x):
        isPresent,y = self.searchNode(x)   #Returns the node where the search ended
        if not isPresent:
            if y.parent == None:    #The only leaf
                newLeafNode = rbTree(x,leaf=True,color = 'b')
                if x < y.data:
                    newInternalNode = rbTree(x,leftChild = newLeafNode,rightChild = y,color = 'b')
                else:
                    newInternalNode = rbTree(x,leftChild = y,rightChild = newLeafNode,color = 'b')

                newLeafNode.parent = newInternalNode

    def searchNode(self,x):
        if x == self.data and self.leaf == True:
            return True,self
        elif x <= self.data:
            if self.leftChild == None or self.leaf:
                return False,self
            else:
                return self.leftChild.searchNode(x)
        else:   #x > self.data
            if self.rightChild == None or self.leaf:
                return False,self
            else:
                return self.rightChild.searchNode(x)

    def deleteNode(self,x):
        pass

t = rbTree(5,'b')
t.insertNode(3)
t.insertNode(7)
print(t.searchNode(3))
