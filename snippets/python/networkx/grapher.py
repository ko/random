#!/usr/local/bin/python2.7

import networkx as nx

G=nx.Graph()

# create nodes
G.add_node('Camera')
G.add_node('DSLR')
G.add_node('6d')
G.add_node('Canon 6d')
G.add_node('Canon')
G.add_node('Canon Inc.')

# create edges between nodes
G.add_edge('Camera', 'DSLR', weight=7)
G.add_edge('DSLR', '6d', weight=2)
G.add_edge('6d', 'Canon 6d', weight=11)
G.add_edge('Canon 6d', 'Canon', weight=20)
G.add_edge('Canon', 'Canon Inc.', weight=30)

G.add_edge('Camera', 'Canon 6d', weight=15)
G.add_edge('DSLR', 'Canon 6d', weight=3)

for n in G.neighbors_iter('6d'):
    rc = G.get_edge_data('6d', n)
    print rc
