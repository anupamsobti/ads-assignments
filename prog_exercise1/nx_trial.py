#!/usr/bin/python3
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

G=nx.path_graph(8)
nx.draw(G)
plt.savefig("simple_path.png") # save as png
plt.show() # display

