#!/usr/bin/python3
import random

def largestValue(node):
    if node.leaf:
        return node.leafData
    else:
        return largestValue(node.rightChild)

def insertInternalNode(node,sibling):   #The sibling from which it was separated and the node itself are inputs
    nodeLargestValue = largestValue(node)
    siblingLargestValue = largestValue(sibling)

    siblingParent = sibling.parent

    #Base case (A new root has to be created)
    if siblingParent == None:
        if nodeLargestValue < siblingLargestValue:
            newNode = TwoThreeTree(leftChild = node,dvalue1 = nodeLargestValue,rightChild = sibling)
        else:
            newNode = TwoThreeTree(leftChild = sibling,dvalue1 = siblingLargestValue,rightChild = node)

        node.parent = newNode
        sibling.parent = newNode

        return True,newNode

    elif siblingParent.dvalue2 == None:    #Parent has only two children
        if siblingParent.leftChild == sibling:
            otherSibling = siblingParent.rightChild
            siblingIsSmaller = True
        else:
            otherSibling = siblingParent.leftChild
            siblingIsSmaller = False

        otherSiblingLargestValue = largestValue(otherSibling)

        if siblingIsSmaller and nodeLargestValue < siblingParent.dvalue1:
            siblingParent.leftChild = node
            node.parent = siblingParent
            siblingParent.dvalue1 = nodeLargestValue
            siblingParent.middleChild = sibling
            siblingParent.dvalue2 = siblingLargestValue

        elif (not siblingIsSmaller) and nodeLargestValue < siblingParent.dvalue1:
            siblingParent.leftChild = node
            node.parent = siblingParent
            siblingParent.dvalue1 = nodeLargestValue
            siblingParent.middleChild = otherSibling
            siblingParent.dvalue2 = otherSiblingLargestValue

        elif node.dvalue1 > siblingParent.dvalue1:
            if siblingParent.rightChild.dvalue1 > node.dvalue1:
                siblingParent.middleChild = node
                node.parent = siblingParent
                siblingParent.dvalue2 = nodeLargestValue
            else:
                siblingParent.middleChild = siblingParent.rightChild
                siblingParent.rightChild = node
                node.parent = siblingParent
                siblingParent.dvalue2 = largestValue(siblingParent.middleChild)  #Can be made more efficient by using siblingIsSmaller

        return False,siblingParent

    else:   #Parent has 3 children
        if node.dvalue1 < siblingParent.leftChild.dvalue1:
            newNode = TwoThreeTree(dvalue1 = nodeLargestValue,leftChild = node,rightChild = siblingParent.leftChild)
            node.parent = newNode
            siblingParent.leftChild.parent = newNode
            siblingParent.leftChild = siblingParent.middleChild
            siblingParent.middleChild = None
            siblingParent.dvalue1 = siblingParent.dvalue2
            siblingParent.dvalue2 = None

            return insertInternalNode(newNode,siblingParent)
        elif node.dvalue1 < siblingParent.dvalue2:
            newNode = TwoThreeTree(dvalue1 = largestValue(siblingParent.leftChild),leftChild = siblingParent.leftChild,rightChild = node)
            node.parent = newNode
            siblingParent.leftChild.parent = newNode
            siblingParent.leftChild = siblingParent.middleChild
            siblingParent.middleChild = None
            siblingParent.dvalue1 = siblingParent.dvalue2
            siblingParent.dvalue2 = None

            return insertInternalNode(newNode,siblingParent)
        else:   #Greater than both dvalue1 and dvalue2
            if node.dvalue1 < siblingParent.rightChild.dvalue1:
                newNode = TwoThreeTree(leftChild = node,rightChild = siblingParent.rightChild,dvalue1 = nodeLargestValue)
                node.parent = newNode
                siblingParent.rightChild.parent = newNode
                siblingParent.dvalue2 = None
                siblingParent.rightChild = siblingParent.middleChild
                siblingParent.middleChild = None

                return insertInternalNode(newNode,siblingParent)
            else:
                newNode = TwoThreeTree(leftChild = siblingParent.rightChild,rightChild = node,dvalue1 = largestValue(siblingParent.rightChild))
                node.parent = newNode
                siblingParent.rightChild.parent = newNode
                siblingParent.dvalue2 = None
                siblingParent.rightChild = siblingParent.middleChild
                siblingParent.middleChild = None

                return insertInternalNode(newNode,siblingParent)


class TwoThreeTree():
    def __init__(self,dvalue1=None,dvalue2=None,leftChild=None,middleChild=None,rightChild=None,parent=None,leaf=False,leafData = None):
        self.dvalue1 = dvalue1
        self.dvalue2 = dvalue2
        self.leftChild = leftChild
        self.middleChild = middleChild
        self.rightChild = rightChild
        self.parent = parent
        self.leaf = leaf
        self.leafData = leafData

    def insert(self,x):
        isPresent,y = self.search(x)  #Returns the leaf containing x or just > x
        #print(x,y.leafData)
        if not isPresent:
            z=y.parent

            #Base Case
            if y.parent == None:    #A single leaf is present in the tree
                nodeForX = TwoThreeTree(leaf = True,leafData = x)   #A new leaf node for X
                if y.leafData <= x:
                    self = TwoThreeTree(dvalue1 = y.leafData,leftChild=y,rightChild=nodeForX)   #Internal node with discriminant value y
                else:
                    self = TwoThreeTree(dvalue1 = x,leftChild = nodeForX,rightChild = y)    #Internal Node with discriminant value x

                nodeForX.parent = self
                y.parent = self
            
            #If the node is inserted in an internal node with 2 children
            elif z.dvalue2 == None:
                nodeForX = TwoThreeTree(leaf=True,leafData = x,parent = z) #New Leaf node for X
                if y == z.leftChild:
                    z.middleChild = y
                    z.leftChild = nodeForX
                    z.dvalue1 = x
                    z.dvalue2 = y.leafData
                elif x < y.leafData:
                    z.middleChild = nodeForX 
                    z.rightChild = y
                    z.dvalue2 = x
                else:
                    z.middleChild = y
                    z.rightChild = nodeForX
                    z.dvalue2 = y.leafData

            #if the node is inserted in an internal node with 3 children
            else:
                nodeForX = TwoThreeTree(leaf=True,leafData = x) #New Leaf node for X
                if x < z.leftChild.leafData:
                    newInternalNode = TwoThreeTree(dvalue1 = x,leftChild = nodeForX,rightChild = z.leftChild)
                    nodeForX.parent = newInternalNode
                    z.leftChild.parent = newInternalNode

                    z.leftChild = z.middleChild
                    z.dvalue1 = z.leftChild.leafData
                    z.dvalue2 = None
                    z.middleChild = None

                    isRootNew,newRoot = insertInternalNode(newInternalNode,z)

                    if isRootNew:
                        self = newRoot
                elif x < z.dvalue2:
                    newInternalNode = TwoThreeTree(leftChild = z.leftChild,dvalue1 = z.dvalue1,rightChild = nodeForX)
                    nodeForX.parent = newInternalNode
                    z.leftChild.parent = newInternalNode

                    z.leftChild = z.middleChild
                    z.dvalue1 = z.dvalue2
                    z.middleChild = None
                    z.dvalue2 = None

                    isRootNew,newRoot = insertInternalNode(newInternalNode,z)
                    if isRootNew:
                        self = newRoot
                elif x < z.rightChild.leafData:
                    newInternalNode = TwoThreeTree(leftChild = nodeForX,dvalue1 = x,rightChild = z.rightChild)
                    nodeForX.parent = newInternalNode
                    z.rightChild.parent = newInternalNode

                    z.rightChild = z.middleChild
                    z.dvalue2 = None
                    z.middleChild = None

                    isRootNew,newRoot = insertInternalNode(newInternalNode,z)
                    if isRootNew:
                        self = newRoot

                else:
                    newInternalNode = TwoThreeTree(leftChild = z.rightChild,dvalue1 = z.rightChild.leafData,rightChild = nodeForX)
                    nodeForX.parent = newInternalNode
                    z.rightChild.parent = newInternalNode

                    z.rightChild = z.middleChild
                    z.dvalue2 = None
                    z.middleChild = None

                    isRootNew,newRoot = insertInternalNode(newInternalNode,z)
                    if isRootNew:
                        self = newRoot

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

    def inOrder(self):
        if self.leftChild != None:
            self.leftChild.inOrder()
        if self.middleChild != None:
            self.middleChild.inOrder()
        if self.leaf:
            print("Leaf ",self.leafData)
        else:
            print("IN Dvalue1 = ",self.dvalue1," Dvalue2 = ",self.dvalue2)
        if self.rightChild != None:
            self.rightChild.inOrder()


    def delete(self,x):
        isPresent,y = self.search(x)  #Returns the leaf containing x or just > x
        if isPresent:
            #Base case
            z = y.parent
            if z == None:    #only node in the tree
                return None
            elif z.parent == None and z.dvalue2 == None: #Only 2 leaves and 1 internal node
                if z.leftChild == y:
                    return z.rightChild
                else:
                    return z.leftChild
            elif z.dvalue2 != None: #3 children
                if y == z.leftChild:
                    z.leftChild = z.middleChild
                    z.middleChild = None
                    z.dvalue1 = z.dvalue2
                    z.dvalue2 = None
                elif y == z.middleChild:
                    z.middleChild = None
                    z.dvalue2 = None
                else:    #y == z.rightChild
                    z.rightChild = z.middleChild
                    z.middleChild = None
                    z.dvalue2 = None

                    node = z
                    while (node.parent != None):    #Updating discriminant values
                        if node == node.parent.leftChild:
                            node.parent.dvalue1 = z.rightChild.leafData
                            break
                        elif node == node.parent.middleChild:
                            node.parent.dvalue2 = z.rightChild.leafData
                            break
                        node = node.parent

            else:   #The node z (parent of y) has 2 children
                if z.parent != None and z.parent.dvalue2 != None:   #z has 2 siblings
                    if z == z.parent.leftChild:
                        #Check if the middle child has 3 leaves. In this case, the other node can borrow one leaf
                        if z.parent.middleChild.dvalue2 != None:
                            if y == z.leftChild:
                                z.leftChild = z.rightChild
                                z.dvalue1 = z.leftChild.leafData
                                z.rightChild = z.parent.middleChild.leftChild
                                z.rightChild.parent = z
                                
                                z.parent.dvalue1 = z.rightChild.leafData    #updated discriminant value of parent
                                
                                z.parent.middleChild.leftChild = z.parent.middleChild.middleChild
                                z.parent.middleChild.dvalue1 = z.parent.middleChild.dvalue2
                                z.parent.middleChild.dvalue2 = None
                                z.parent.middleChild.middleChild = None
                            else:
                                z.rightChild = z.parent.middleChild.leftChild
                                z.rightChild.parent = z
                                z.parent.middleChild.dvalue1 = z.parent.middleChild.dvalue2
                                z.parent.middleChild.dvalue2 = None
                                z.parent.middleChild.leftChild = z.parent.middleChild.middleChild
                                z.parent.middleChild.middleChild = None

                                z.parent.dvalue1 = z.rightChild.leafData    #updated discriminant value of parent

                        elif z.parent.middleChild.dvalue2 == None: #If it has 2 leaves, the remaining node can merge with the middleChild
                            z.parent.middleChild.middleChild = z.parent.middleChild.leftChild
                            z.parent.middleChild.dvalue2 = z.parent.middleChild.middleChild.leafData
                            if y == z.leftChild:
                                z.parent.middleChild.leftChild = z.rightChild
                            else:
                                z.parent.middleChild.leftChild = z.leftChild
                            z.parent.middleChild.dvalue1 = z.parent.middleChild.leftChild.leafData
                            z.parent.leftChild = z.parent.middleChild
                            z.parent.dvalue1 = z.parent.dvalue2
                            z.parent.dvalue2 = None
                            z.parent.middleChild = None

                    elif z == z.parent.middleChild: #If z was the middleChild
                        if z.parent.leftChild.dvalue2 != None:  #The leftchild had 3 children
                            leftSibling = z.parent.leftChild
                            if y == z.leftChild:
                                z.leftChild = leftSibling.rightChild
                                z.leftChild.parent = z
                                z.dvalue1 = z.leftChild.leafData
                                leftSibling.rightChild = leftSibling.middleChild
                                leftSibling.parent.dvalue1 = leftSibling.rightChild.leafData
                                leftSibling.dvalue2 = None
                                leftSibling.middleChild = None
                            else:   #y == z.rightChild
                                z.rightChild = z.leftChild
                                z.parent.dvalue2 = z.rightChild.leafData
                                z.leftChild = leftSibling.rightChild
                                z.leftChild.parent = z
                                z.dvalue1 = z.leftChild.leafData
                                leftSibling.rightChild = leftSibling.middleChild
                                leftSibling.dvalue2 = None
                                leftSibling.middleChild = None
                                leftSibling.parent.dvalue1 = leftSibling.rightChild.leafData
                        elif z.parent.rightChild.dvalue2 != None:   #The right child had 3 children
                            rightSibling = z.parent.rightChild
                            if y == z.leftChild:
                                z.leftChild = z.rightChild
                                z.dvalue1 = z.leftChild.leafData
                                z.rightChild = rightSibling.leftChild
                                z.rightChild.parent = z
                                z.parent.dvalue2 = z.rightChild.leafData
                                rightSibling.leftChild = rightSibling.middleChild
                                rightSibling.dvalue1 = rightSibling.leftChild.leafData
                                rightSibling.middleChild = None
                                rightSibling.dvalue2 = None
                            else:   #y == z.rightChild
                                z.rightChild = rightSibling.leftChild
                                z.parent.dvalue2 = z.rightChild.leafData
                                z.rightChild.parent = z
                                rightSibling.leftChild = rightSibling.middleChild
                                rightSibling.dvalue1 = rightSibling.leftChild.leafData
                                rightSibling.dvalue2 = None
                                rightSibling.middleChild = None
                        else:   #Both siblings have 2 children each (One of the siblings has to merge with the middle child)    --> Merging with the leftChild
                            leftSibling  = z.parent.leftChild
                            if y == z.leftChild:
                                leftSibling.middleChild = leftSibling.rightChild
                                leftSibling.dvalue2 = leftSibling.middleChild.leafData
                                leftSibling.rightChild = z.rightChild
                                leftSibling.rightChild.parent = leftSibling
                                z.parent.dvalue1 = leftSibling.rightChild.leafData
                                z.parent.middleChild = None
                                z.parent.dvalue2 = None
                            else:   #if y == z.rightChild
                                leftSibling.middleChild = leftSibling.rightChild
                                leftSibling.dvalue2 = leftSibling.middleChild.leafData
                                leftSibling.rightChild = z.leftChild
                                leftSibling.rightChild.parent = leftSibling
                                z.parent.dvalue1 = leftSibling.rightChild.leafData
                                z.parent.middleChild = None
                                z.parent.dvalue2 = None

                    elif z == z.parent.rightChild:  #If z was the rightChild
                        middleSibling = z.parent.middleChild
                        if middleSibling.dvalue2 != None:   #There are 3 children, the right Sibling borrows one
                            if y == z.leftChild:
                                z.leftChild = middleSibling.rightChild
                                z.leftChild.parent = z
                                z.dvalue1 = z.leftChild.leafData
                                middleSibling.rightChild = middleSibling.middleChild
                                middleSibling.parent.dvalue2 = middleSibling.rightChild.leafData
                                middleSibling.dvalue2 = None
                                middleSibling.middleChild = None
                            else:   #if y == z.rightChild:
                                z.rightChild = z.leftChild
                                z.leftChild = middleSibling.rightChild
                                z.leftChild.parent = z
                                z.dvalue1 = z.leftChild.leafData
                                middleSibling.rightChild = middleSibling.middleChild
                                middleSibling.parent.dvalue2 = middleSibling.rightChild.leafData
                                middleSibling.dvalue2 = None
                                middleSibling.middleChild = None
                                
                                node = z
                                while (node.parent != None):    #Updating discriminant values
                                    if node == node.parent.leftChild:
                                        node.parent.dvalue1 = z.rightChild.leafData
                                        break
                                    elif node == node.parent.middleChild:
                                        node.parent.dvalue2 = z.rightChild.leafData
                                        break
                                    node = node.parent

                        elif middleSibling.dvalue2 == None: #The middle sibling also has only 2 children => The middle sibling must merge with the right child (z)
                            middleSibling.middleChild = middleSibling.rightChild
                            middleSibling.dvalue2 = middleSibling.middleChild.leafData
                            middleSibling.parent.dvalue2 = None
                            middleSibling.parent.middleChild = None
                            if y == z.leftChild:
                                middleSibling.rightChild = z.rightChild
                            else:
                                middleSibling.rightChild = z.leftChild
                            middleSibling.rightChild.parent = middleSibling
                            z = middleSibling
                            
                            node = z
                            while (node.parent != None):    #Updating discriminant values
                                if node == node.parent.leftChild:
                                    node.parent.dvalue1 = z.rightChild.leafData
                                    break
                                elif node == node.parent.middleChild:
                                    node.parent.dvalue2 = z.rightChild.leafData
                                    break
                                node = node.parent


                #TODO: z has 1 sibling
                if z == z.parent.leftChild:
                    pass

                else:   #if z = rightChild
                    pass




            return self


myTree = TwoThreeTree(leaf=True,leafData=8)
myTree = myTree.insert(5)
myTree = myTree.insert(4)
myTree = myTree.insert(9)
myTree = myTree.insert(3)
myTree = myTree.insert(6)
#myTree = myTree.insert(10)
#myTree = myTree.insert(0)

#for i in range(1000):
#    myTree = myTree.insert(random.randrange(-1000,1000))
myTree.inOrder()
myTree = myTree.delete(5)

print(myTree.search(3))
myTree.inOrder()
