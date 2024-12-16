# ####################### NOTE: ###########################
# This is an extended feature or additional code
# for Task 4a designed to ensure that, even after
# line closures, the network of stations remains connected.
# #########################################################

import pandas as pd
import sys
import networkx as nx
import matplotlib.pyplot as plt

# Add the path to the code library
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary functions and classes
from mst import kruskal
from adjacency_list_graph import AdjacencyListGraph

# Load the London Underground dataset
file_path = 'London Underground Data.xlsx'
underground_data = pd.read_excel(file_path, usecols=[0, 1, 2, 3], names=["Line", "Station1", "Station2", "JourneyTime"])

# Filter rows where both 'Station2' and 'JourneyTime' are filled, indicating direct connections with journey times
connections_data = underground_data.dropna(subset=["Station2", "JourneyTime"])

# Create an adjacency list graph
stations = set(connections_data["Station1"]).union(set(connections_data["Station2"]))
station_to_index = {station: index for index, station in enumerate(stations)}
index_to_station = {index: station for station, index in station_to_index.items()}
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

# Add edges to the graph, checking for duplicates
edges = []
for _, row in connections_data.iterrows():
    station1 = row["Station1"]
    station2 = row["Station2"]
    journey_time = row["JourneyTime"]
    u = station_to_index[station1]
    v = station_to_index[station2]

    if u != v:  # Ensure no self-loops
        if not graph.has_edge(u, v):
            edges.append((journey_time, u, v))
            graph.insert_edge(u, v, journey_time)

# Compute the Minimum Spanning Tree (MST) using Kruskal's algorithm
mst_graph = kruskal(graph)

# Calculate the total weight of the MST by summing the weights of its edges
total_weight = sum(edge.get_weight() for u in range(mst_graph.get_card_V()) for edge in mst_graph.get_adj_list(u)) // 2
print(f"Total weight of the MST: {total_weight}")

# Find the edges in the MST and store them in a set for comparison
mst_edge_set = set()
for u in range(mst_graph.get_card_V()):
    for edge in mst_graph.get_adj_list(u):
        v = edge.get_v()
        if u < v:  # Include each edge only once to avoid duplicates
            mst_edge_set.add((u, v))

# Find redundant edges
all_edge_set = set((min(u, v), max(u, v)) for _, u, v in edges)
redundant_edges = all_edge_set - mst_edge_set

# Output redundant edges (edges that can be closed)
print("List of line sections that can be closed (redundant edges):")
for u, v in redundant_edges:
    station_u = index_to_station[u]
    station_v = index_to_station[v]
    print(f"{station_u} -- {station_v}")

# Create a NetworkX graph from the MST
G_mst = nx.Graph()
for u, v in mst_edge_set:
    G_mst.add_edge(u, v)

# Create a NetworkX graph from the original graph
G_all = nx.Graph()
for _, u, v in edges:
    G_all.add_edge(u, v)

# Check if the MST graph is connected
if nx.is_connected(G_mst):
    print("The MST graph is connected. All stations can still be reached.")
else:
    print("The MST graph is not connected. Some stations cannot be reached.")

# Visualize the graph
pos = nx.spring_layout(G_all)
plt.figure(figsize=(10, 5))
nx.draw_networkx_edges(G_all, pos, edge_color='lightgray')
nx.draw_networkx_edges(G_mst, pos, edge_color='black')
nx.draw_networkx_nodes(G_all, pos, node_color='lightblue', node_size=500)
nx.draw_networkx_labels(G_all, pos, labels=index_to_station, font_size=10)

plt.title("Minimum Spanning Tree of the London Underground Network with Redundant Edges")
plt.show()




############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
