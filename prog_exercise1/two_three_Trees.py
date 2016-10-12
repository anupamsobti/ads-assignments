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
        self.leafData = leafData

    def insert(self,x):
        isPresent,y = self.search(x)  #Returns the leaf containing x or just > x
        if not isPresent:
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
                z = y.parent
                nodeForX = TwoThreeTree(leaf=True,leafData = x,parent = z) #New Leaf node for X
                z.middleChild = nodeForX 
                z.rightChild = y
                z.dvalue2 = x

            #if the node is inserted in an internal node with 3 children
            else:
                z = y.parent
                nodeForX = TwoThreeTree(leaf=True,leafData = x,parent = z) #New Leaf node for X
                if x < z.leftChild.leafData:
                    newInternalNode = TwoThreeTree(dvalue1 = x,leftChild = nodeForX,rightChild = z.leftChild)
                    nodeForX.parent = newInternalNode
                    z.leftChild.parent = newInternalNode

                    z.leftChild = z.middleChild
                    z.dvalue1 = z.leftChild.leafData
                    z.dvalue2 = None
                    z.middleChild = None

                    ##Insert Internal Node to the sibling

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

            return newNode

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
                    siblingParent.dvalue2 = largestValue(siblingParent.rightChild)  #Can be made more efficient by using siblingIsSmaller

            return siblingParent

        else:   #Parent has 3 children
            pass



    def largestValue(node):
        if node.leaf:
            return node.leafData
        else:
            return largestValue(node.rightChild)

    def delete(self,x):
        pass

myTree = TwoThreeTree(leaf=True,leafData=4)
myTree = myTree.insert(5)
print(myTree.search(5))
