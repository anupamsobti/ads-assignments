#!/usr/bin/python3
import random
import matplotlib.pyplot as plt
import networkx as nx

#Drawing Functions
def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, 
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    #if parent != None:
    #    neighbors.remove(parent)
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos


def createDiagram(tree,root):
    G = nx.DiGraph()
    populateNode(G,tree)

    plt.title("NX Tree")
    pos = hierarchy_pos(G,root)
    nx.draw_networkx(G,pos)
    plt.show()

def populateNode(G,treeNode):
    G.add_node(treeNode.data)
    if treeNode.leftChild != None:
        populateNode(G,treeNode.leftChild)
        G.add_edge(treeNode.data,treeNode.leftChild.data)
    if treeNode.rightChild != None:
        populateNode(G,treeNode.rightChild)
        G.add_edge(treeNode.data,treeNode.rightChild.data)


#AVL Tree class
class AVLTree:
    def __init__(self,data=None,height=1,leftChild = None,rightChild = None,parent = None):
        self.data = data
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.parent = parent
        self.height = height
        
    def inorder(self):
        if self.leftChild != None:
            self.leftChild.inorder()
        print(self.data," ",end= "")
        if self.rightChild != None:
            self.rightChild.inorder()

    def inorderWithHeight(self):
        if self.leftChild != None:
            self.leftChild.inorderWithHeight()
        print("(d=" + str(self.data) + ",h=" + str(self.height) + ")",end= "")
        if self.rightChild != None:
            self.rightChild.inorderWithHeight()
                
    def postOrder(self):
        if self.leftChild != None:
            self.leftChild.postOrder()
        if self.rightChild != None:
            self.rightChild.postOrder()
        print(self.data,end = "")
    
    def isNodeBalanced(self):
        if self.leftChild == None and self.rightChild == None:
            return True
        elif self.leftChild == None:
            if self.rightChild.height < 2:
                return True
            else:
                return False
        elif self.rightChild == None:
            if self.leftChild.height < 2:
                return True
            else:
                return False
        else:
            if abs(self.rightChild.height - self.leftChild.height) < 2:
                return True
            else:
                return False
    
    def isTreeBalanced(self):
        if not self.isNodeBalanced():
            return False
        if self.leftChild != None:
            if not self.leftChild.isTreeBalanced():
                return False
        if self.rightChild != None:
            if not self.rightChild.isTreeBalanced():
                return False
        return True

    def searchNode(self,value):
        if value == self.data:
            return True,self
        elif value < self.data:
            if self.leftChild == None:
                return False,self
            else:
                return self.leftChild.searchNode(value)
        else:   #Value > self.data
            if self.rightChild == None:
                return False,self
            else:
                return self.rightChild.searchNode(value)

    def insertNode(self,value):
        isPresent,node = self.searchNode(value)
        if not isPresent:
            if value > node.data:
                node.rightChild = AVLTree(data = value,parent = node)
                newNode = node.rightChild
            else:   #value < node.data
                node.leftChild = AVLTree(data = value,parent = node)
                newNode = node.leftChild

            updateHeights(node)
            isRootNew,newRoot = balanceFromNode(newNode)
            if isRootNew:
                if newRoot == None:
                    print("shit")
                return newRoot
            else:
                return self
        else:
            return self

    def deleteNode(self,value):

        def predecessor(node):
            a = node.leftChild
            while a.rightChild != None:
                a = a.rightChild
            return a

        isPresent,node = self.searchNode(value)
        if isPresent:
            #Base case:
            if node.parent == None and node.leftChild == None and node.rightChild == None:
                return None #Deleted the root itself
            elif node.leftChild == None and node.rightChild == None:
                #print("Deleting ",node.data)
                k = node.parent
                if node == k.leftChild:
                    k.leftChild = None
                else:
                    k.rightChild = None

                updateHeights(k)
                #print(k.data,balanceFromNode_deletion(k))
                isRootNew,newRoot = balanceFromNode_deletion(k)
                if isRootNew:
                    self = newRoot
            elif node.leftChild == None:
                k = node.parent
                if node == k.leftChild:
                    k.leftChild = node.rightChild
                    node.rightChild.parent = k
                    updateHeights(k)
                else:   #node == k.rightChild
                    k.rightChild = node.rightChild
                    node.rightChild.parent = k
                    updateHeights(k)

                isRootNew,newRoot = balanceFromNode_deletion(k)
                if isRootNew:
                    self = newRoot
            elif node.rightChild == None:
                k = node.parent
                if node == k.leftChild:
                    k.leftChild = node.leftChild
                    node.leftChild.parent = k
                else:
                    k.rightChild = node.leftChild
                    node.leftChild.parent = k
                updateHeights(k)

                isRootNew,newRoot = balanceFromNode_deletion(k)
                if isRootNew:
                    self = newRoot
            else:   #A node with both children
                predecessorNode = predecessor(node)
                #node.data = predecessorNode.data
                #return self.deleteNode(predecessorNode.data)
                self = self.deleteNode(predecessorNode.data)
                node.data = predecessorNode.data
                return self

        return self

def balanceFromNode_deletion(node):
    isTreeBalanced,nodes = checkSubtreeBalance_deletion(node)
    #print(checkSubtreeBalance_deletion(node))
    if not isTreeBalanced:
        z = nodes[2]
        if z.parent == None:    #Base case - Only 3 elements
            return True,rotate(nodes[0],nodes[1],nodes[2])
        else:   #z has a parent
            z = rotate(nodes[0],nodes[1],nodes[2])
            return balanceFromNode_deletion(z)
            #return False,z
    else:
        return False,node

def balanceFromNode(node):
    isTreeBalanced,nodes = checkSubtreeBalance(node)
    #print(nodes)
    if not isTreeBalanced:
        z = nodes[2]
        if z.parent == None:    #Base case - Only 3 elements
            return True,rotate(nodes[0],nodes[1],nodes[2])
        else:   #z has a parent
            z = rotate(nodes[0],nodes[1],nodes[2])
            return False,z
    else:
        return False,node

def updateHeights(node):    #To be further optimized. Stop when height = required height
    while node != None:
        if node.leftChild != None and node.rightChild != None:
            node.height = max(node.leftChild.height,node.rightChild.height) + 1
        elif node.leftChild != None:
            node.height = node.leftChild.height + 1
        elif node.rightChild != None:
            node.height = node.rightChild.height + 1
        else:
            node.height = 1
        node = node.parent

def checkSubtreeBalance(node):
    x = node
    y = node.parent
    if y == None:
        return True,node
    else:
        z = node.parent.parent
        if z == None:
            return True,node
        else:
            while z != None:
                if not z.isNodeBalanced():
                    return False,(x,y,z)
                z = z.parent
                y = y.parent
                x = x.parent
            return True,node

def checkSubtreeBalance_deletion(node):
    z = node
    while z != None:
        if not z.isNodeBalanced():
            if z.leftChild != None and z.rightChild != None:
                if z.leftChild.height >= z.rightChild.height:
                    y = z.leftChild
                elif z.leftChild.height < z.rightChild.height:
                    y = z.rightChild
            elif z.leftChild == None:
                y = z.rightChild
            elif z.rightChild == None:
                y = z.leftChild
            else:
                print("not possible")
            
            if y.leftChild != None and y.rightChild != None:
                if y.leftChild.height >= y.rightChild.height:
                    x = y.leftChild
                elif y.leftChild.height < y.rightChild.height:
                    x = y.rightChild
            elif y.leftChild == None:
                x = y.rightChild
            elif y.rightChild == None:
                x = y.leftChild
            else:
                print("not possible")

            return False,(x,y,z)
        z = z.parent
    return True,node

#Figures out which case it is and balances the tree
def rotate(nodeX,nodeY,nodeZ):
    if nodeZ.leftChild != None and nodeZ.leftChild.leftChild != None and nodeX == nodeZ.leftChild.leftChild:
        #Case 1
        nodeY.parent = nodeZ.parent
        if nodeZ.parent != None and nodeZ.parent.leftChild != None:
            if nodeZ == nodeZ.parent.leftChild:
                nodeZ.parent.leftChild = nodeY
        if nodeZ.parent != None and nodeZ.parent.rightChild != None:
            if nodeZ.parent.rightChild == nodeZ:
                nodeZ.parent.rightChild = nodeY
            
        nodeZ.leftChild = nodeY.rightChild
        if nodeY.rightChild != None:
            nodeY.rightChild.parent = nodeZ
        
        nodeY.rightChild = nodeZ
        nodeZ.parent = nodeY

        #Updating heights
        nodeZ.height -= 2

        updateHeights(nodeY.parent)
        
        #print("Rotation Case 1: ",nodeY.data)

        return nodeY

    elif nodeZ.leftChild != None and nodeZ.leftChild.rightChild != None and nodeX == nodeZ.leftChild.rightChild:
        #Case 2
        nodeX.parent = nodeZ
        nodeZ.leftChild = nodeX
        
        nodeY.rightChild = nodeX.leftChild
        if nodeX.leftChild != None:
            nodeX.leftChild.parent = nodeY
        
        nodeX.leftChild = nodeY
        nodeY.parent = nodeX

        nodeY.height -= 1
        nodeX.height += 1

        #print("Rotation Case 3")
        
        return rotate(nodeY,nodeX,nodeZ)
 
    elif nodeZ.rightChild != None and nodeZ.rightChild.rightChild != None and nodeX == nodeZ.rightChild.rightChild:
        #Case 3
        nodeY.parent = nodeZ.parent
        if nodeZ.parent != None and nodeZ.parent.leftChild != None:
            if nodeZ == nodeZ.parent.leftChild:
                nodeZ.parent.leftChild = nodeY
        if nodeZ.parent != None and nodeZ.parent.rightChild != None:
            if nodeZ == nodeZ.parent.rightChild:
                nodeZ.parent.rightChild = nodeY
            
        nodeZ.rightChild = nodeY.leftChild
        if nodeY.leftChild != None:
            nodeY.leftChild.parent = nodeZ
        
        nodeY.leftChild = nodeZ
        nodeZ.parent = nodeY

        nodeZ.height -=2
        updateHeights(nodeY.parent)

        #print("Rotation Case 2 : ",nodeY.data)

        return nodeY
 
    elif nodeZ.rightChild != None and nodeZ.rightChild.leftChild != None and nodeX == nodeZ.rightChild.leftChild:
        #Case 4
        nodeX.parent = nodeZ.rightChild
        nodeZ.rightChild = nodeX
        
        nodeY.leftChild = nodeX.rightChild
        if nodeX.rightChild != None:
            nodeX.rightChild.parent = nodeY
        
        nodeX.rightChild = nodeY
        nodeY.parent = nodeX
        
        nodeY.height -= 1
        nodeX.height += 1

        #print("Rotation case 4")

        return rotate(nodeY,nodeX,nodeZ)

    else:
        print("Couldn't figure out case")

myTree = AVLTree(2)
#print ("After inserting 2 : ")
#myTree.inorder()

#for i in range(101):
#    #print(i)
#    myTree = myTree.insertNode(i)

#myTree = myTree.insertNode(0)
#myTree = myTree.insertNode(1)

#print("Inserting 3.")
#myTree = myTree.insertNode(3)
#print(myTree.searchNode(3))
#print ("Inserting 5.")
#myTree = myTree.insertNode(5)
#print("Inserting 1")
#myTree = myTree.insertNode(1)
#print("Inserting 4")
#myTree = myTree.insertNode(6)
#myTree = myTree.insertNode(7)
#myTree = myTree.insertNode(8)
#print("Inserting -1")
#myTree = myTree.insertNode(-1)
#myTree = myTree.deleteNode(3)
#myTree = myTree.deleteNode(5)
##print("After inserting 3,5,1,4,-1")

for i in range(100):
    myTree = myTree.insertNode(random.randrange(100))

for i in range(20):
    myTree = myTree.deleteNode(random.randrange(100))

myTree.inorderWithHeight()
print("")
#print(myTree.isTreeBalanced())
createDiagram(myTree,myTree.data)
