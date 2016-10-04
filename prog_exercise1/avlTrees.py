#!/usr/bin/python3
import matplotlib.pyplot as plt
import networkx as nx

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

    def insertNode(self,value):
        if value <= self.data:
            if self.leftChild == None:
                self.leftChild = AVLTree(value)
                self.leftChild.parent = self

                updateHeights(self.leftChild,self.leftChild.height)
                #balanceFromNode(self.leftChild)    
            else:
                self.leftChild.insertNode(value)
        else:
            if self.rightChild == None:
                self.rightChild = AVLTree(value)
                self.rightChild.parent = self
                
                updateHeights(self.rightChild,self.rightChild.height)
                #balanceFromNode(self.rightChild)
                
            else:
                self.rightChild.insertNode(value)

def balanceFromNode(node):
    balancingResult = checkSubtreeBalance(node)
    print ("Balancing from node", node.data)
    if (not balancingResult[0]) and node.parent != None:
        while node.parent.parent != balancingResult[1]:
            node=node.parent
        resultingRoot = rotate(node,node.parent,node.parent.parent)
        print ("Resulting root : ", resultingRoot.data)
        balanceFromNode(resultingRoot)

#Update Heights
def updateHeights(node,seed):
    i=0
    while True:
        if node.height < seed+i:
            node.height += 1
        if node.parent == None:
            break
        else:
            node = node.parent
            i+=1
#Logic for checking balancing
def checkSubtreeBalance(node):
    firstImbalanced = None
    while True:
        if node.isNodeBalanced():
            balanced = True
        else:
            balanced = False
            firstImbalanced = node
            break
        
        if node.parent == None:
            break
        else:
            node = node.parent
    
    return balanced,firstImbalanced

#Figures out which case it is and balances the tree
def rotate(nodeX,nodeY,nodeZ):
    if nodeZ.leftChild != None:
        if nodeZ.leftChild.leftChild != None:
            if nodeX == nodeZ.leftChild.leftChild: #Case 1
                
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
                
                return nodeY

        elif nodeX == nodeZ.leftChild.rightChild: #Case 3
            nodeX.parent = nodeZ
            nodeZ.leftChild = nodeX
            
            nodeY.rightChild = nodeX.leftChild
            if nodeX.leftChild != None:
                nodeX.leftChild.parent = nodeY
            
            nodeX.leftChild = nodeY
            nodeY.parent = nodeX
        
            rotate(nodeY,nodeX,nodeZ)
            
    elif nodeZ.rightChild != None:
        if nodeZ.rightChild.rightChild != None:
            if nodeX == nodeZ.rightChild.rightChild: #Case 2
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
                
                return nodeY
    
        elif nodeX == nodeZ.rightChild.leftChild: #Case 4
            nodeX.parent = nodeZ.rightChild
            nodeZ.rightChild = nodeX
            
            nodeY.leftChild = nodeX.rightChild
            if nodeX.rightChild != None:
                nodeX.rightChild.parent = nodeY
            
            nodeX.rightChild = nodeY
            nodeY.parent = nodeX
            
            rotate(nodeY,nodeX,nodeZ)
    else:
        print ("Couldn't figure out case.")

myTree = AVLTree(2)
#print ("After inserting 2 : ")
#myTree.inorder()
print("Inserting 3.")
myTree.insertNode(3)
print ("Inserting 5.")
myTree.insertNode(5)
print("Inserting 1")
myTree.insertNode(1)
print("Inserting 4")
myTree.insertNode(4)
print("Inserting -1")
myTree.insertNode(-1)
#print("After inserting 3,5,1,4,-1")
myTree.inorderWithHeight()
print("")
print(myTree.isTreeBalanced())
createDiagram(myTree,2)
