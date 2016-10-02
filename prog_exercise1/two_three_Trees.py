#!/usr/bin/python3
class TwoThreeTree():
    def __init__(self,dvalue1=None,dvalue2=None,leftChild=None,middleChild=None,rightChild=None,parent=None,leaf=False,leafData = None):
        self.dvalue1 = dvalue1
        self.dvalue2 = dvalue2
        self.leftChild = leftChild
        self.middleChild = middleChild
        self.rightChild = rightChild
        self.parent = parent
        self.leaf = leaf
        if self.leaf:
            self.leafData = leafData
        else:   #Useful while finding out largest value in subtree (during inserts)
            temp = self
            while temp.rightChild != None:
                temp = temp.rightChild
            self.leafData = temp.leafData

    def insert(self,x):
        isPresent,y = self.search(x)  #Returns the leaf containing x or just > x
        if not isPresent:
            if y.parent == None:
                nodeForX = TwoThreeTree(leaf = True,leafData = x)
                if y.leafData <= x:
                    self = TwoThreeTree(dvalue1 = y.leafData,leftChild=y,rightChild=nodeForX)
                else:
                    self = TwoThreeTree(dvalue1 = x,leftChild = nodeForX,rightChild = y)

                nodeForX.parent = self
                y.parent = self

        return self


    def search(self,x):
        if self.leaf:
            if self.leafData == x:
                return True,self
            else:
                return False,self
        elif x <= self.dvalue1:
            return self.leftChild.search(x)
        elif self.dvalue2 != None and x < self.dvalue2:
            return self.middleChild.search(x)
        else:
            return self.rightChild.search(x)

    def delete(self,x):
        pass

myTree = TwoThreeTree(leaf=True,leafData=4)
myTree = myTree.insert(5)
print(myTree.search(5))
