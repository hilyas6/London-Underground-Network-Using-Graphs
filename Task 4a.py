import pandas as pd
import sys

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from mst import kruskal # Import the kruskal's code to get the mst
from adjacency_list_graph import AdjacencyListGraph # Graph data structure for adjacency list representation

# Load the London Underground data
file_path = 'London Underground Data.xlsx' #File name in PyCharm directory of data
underground_data = pd.read_excel(file_path, usecols=[0, 1, 2, 3], names=["Line", "Station1", "Station2", "JourneyTime"])

# Filter rows where both 'Station2' and 'JourneyTime' are filled, indicating direct connections with journey times
connections_data = underground_data.dropna(subset=["Station2", "JourneyTime"])
connections_data = connections_data[connections_data["Station1"] != connections_data["Station2"]]

# Create an adjacency list graph
# Define a set of unique stations and map each station to a unique index
stations = set(connections_data["Station1"]).union(set(connections_data["Station2"]))
station_to_index = {station: index for index, station in enumerate(stations)}
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

# Add edges to the graph, checking for duplicates
edges = []  # List to store edges for reference
for _, row in connections_data.iterrows():
    station1 = row["Station1"]
    station2 = row["Station2"]
    journey_time = row["JourneyTime"]
    u = station_to_index[station1]  # Get index for station1
    v = station_to_index[station2]  # Get index for station2

    # Check if the edge already exists in the graph to avoid duplicates
    if not graph.has_edge(u, v):
        edges.append((journey_time, station1, station2))  # Store edge details for later reference
        graph.insert_edge(u, v, journey_time)  # Add edge to the graph

# Compute the Minimum Spanning Tree (MST) using Kruskal's algorithm
mst_graph = kruskal(graph)  # The MST graph returned from the Kruskal function

# Calculate the total weight of the MST by summing the weights of its edges
total_weight = sum(edge.get_weight() for u in range(mst_graph.get_card_V()) for edge in mst_graph.get_adj_list(u)) // 2
print(f"Total weight of the MST: {total_weight}")

# Find the edges in the MST and store them in a set for comparison
mst_edge_set = set()
for u in range(mst_graph.get_card_V()):
    for edge in mst_graph.get_adj_list(u):
        v = edge.get_v()
        if u < v:  # Include each edge only once to avoid duplicates
            mst_edge_set.add((min(u, v), max(u, v)))

# Find redundant edges
# Create a set of all original edges in the graph and identify those not in the MST
all_edge_set = set((min(station_to_index[u], station_to_index[v]), max(station_to_index[u], station_to_index[v])) for _, u, v in edges)
redundant_edges = all_edge_set - mst_edge_set  # Edges that are not in the MST

# Output redundant edges (edges that can be closed)
print("List of line sections that can be closed (redundant edges):")
for u, v in redundant_edges:
    # Convert indices back to station names for display
    station_u = [station for station, index in station_to_index.items() if index == u][0]
    station_v = [station for station, index in station_to_index.items() if index == v][0]
    print(f"{station_u} -- {station_v}")



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
