#!/usr/bin/python3
import networkx as nx
from matplotlib import pyplot as plt

class rbTree():
    def __init__(self,data,color,parent=None,leftChild=None,rightChild=None):
        self.data = data
        self.color = color
        self.parent = parent
        self.leftChild = leftChild
        self.rightChild = rightChild

    def insertNode(self,x):
        y = self.searchNode(x)   #Returns the node where the search ended
        if y.parent == None:
            if x <= y.data:
                y.leftChild = rbTree(x,'b')
                y.leftChild.parent = y
            else:
                y.rightChild = rbTree(x,'b')
                y.rightChild.parent = y


    def searchNode(self,x):
        return self

    def deleteNode(self,x):
        pass



def createDiagram(tree):

    def populateNode(G,treeNode):
        G.add_node(treeNode.data)
        if treeNode.leftChild != None:
            populateNode(G,treeNode.leftChild)
            G.add_edge(treeNode.data,treeNode.leftChild.data)
        if treeNode.rightChild != None:
            populateNode(G,treeNode.rightChild)
            G.add_edge(treeNode.data,treeNode.rightChild.data)

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

    G = nx.DiGraph()
    populateNode(G,tree)
    plt.title("NX Tree")
    pos = hierarchy_pos(G,5)
    nx.draw_networkx(G,pos)
    plt.show()

t = rbTree(5,'b')
t.insertNode(3)
t.insertNode(7)
createDiagram(t)
