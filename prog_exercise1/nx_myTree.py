#!/usr/bin/python3
import matplotlib.pyplot as plt
import networkx as nx

class Tree():
    def __init__(self,data,leftChild=None,rightChild=None):
        self.data = data
        self.leftChild = leftChild
        self.rightChild = rightChild

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
    if parent != None:
        neighbors.remove(parent)
    if len(neighbors)!=0:
        dx = width/len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap, 
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos, 
                                parent = root)
    return pos

def createDiagram(tree):
    G = nx.DiGraph()
    populateNode(G,tree)
    # write dot file to use with graphviz
    # run "dot -Tpng test.dot >test.png"
    #nx.nx_agraph.write_dot(G,'test.dot')
    #
    ## same layout using matplotlib with no labels
    #plt.title("draw_networkx")
    #pos=nx.graphviz_layout(G,prog='dot')
    #nx.draw(G,pos,with_labels=False,arrows=False)
    #plt.savefig('nx_test.png')


    plt.title("NX Tree")
    nx.draw_networkx(G)
    #pos = hierarchy_pos(G,5)
    #nx.draw(G,5,pos=pos,with_labels=True)
    plt.show()

def populateNode(G,treeNode):
    G.add_node(treeNode.data)
    if treeNode.leftChild != None:
        populateNode(G,treeNode.leftChild)
        G.add_edge(treeNode.data,treeNode.leftChild.data)
    if treeNode.rightChild != None:
        populateNode(G,treeNode.rightChild)
        G.add_edge(treeNode.data,treeNode.rightChild.data)

t = Tree(5)
t.leftChild = Tree(4)
t.rightChild = Tree(3)
t.leftChild.leftChild = Tree(1)
t.leftChild.rightChild = Tree(0)
createDiagram(t)
