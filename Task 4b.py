import pandas as pd
import matplotlib.pyplot as plt
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

# Create the reduced graph by removing redundant edges
stations = set(connections_data["Station1"]).union(set(connections_data["Station2"]))
station_to_index = {station: index for index, station in enumerate(stations)}
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

edges = []
for _, row in connections_data.iterrows():
    station1 = row["Station1"]
    station2 = row["Station2"]
    journey_time = row["JourneyTime"]
    u = station_to_index[station1]
    v = station_to_index[station2]

    # Check if the edge already exists to avoid duplicates
    if u != v:
        if not graph.has_edge(u, v):
            edges.append((u, v, journey_time))
            graph.insert_edge(u, v, journey_time)

# Find the MST using Kruskal's algorithm and get redundant edges
mst_graph = kruskal(graph)
mst_edges = set()
for u in range(mst_graph.get_card_V()):
    for edge in mst_graph.get_adj_list(u):
        v = edge.get_v()
        if u < v:
            mst_edges.add((u, v))

all_edges = set((u, v) if u < v else (v, u) for u, v, _ in edges)
redundant_edges = all_edges - mst_edges

# Create the reduced graph without redundant edges
reduced_graph = {}
for _, row in connections_data.iterrows():
    station1 = row["Station1"]
    station2 = row["Station2"]
    journey_time = row["JourneyTime"]
    u, v = station_to_index[station1], station_to_index[station2]

    if (min(u, v), max(u, v)) not in redundant_edges:
        if station1 not in reduced_graph:
            reduced_graph[station1] = {}
        if station2 not in reduced_graph:
            reduced_graph[station2] = {}
        reduced_graph[station1][station2] = journey_time
        reduced_graph[station2][station1] = journey_time

# Calculate journey durations and longest path in the reduced network

def dijkstra_shortest_path(graph, start):
    distances = {station: float('inf') for station in graph}
    distances[start] = 0
    predecessors = {station: None for station in graph}
    visited = set()

    while len(visited) < len(graph):
        # Find the unvisited node with the smallest distance
        min_distance = float('inf')
        min_station = None
        for station in distances:
            if station not in visited and distances[station] < min_distance:
                min_distance = distances[station]
                min_station = station

        if min_station is None:
            break

        visited.add(min_station)

        for neighbor, weight in graph[min_station].items():
            if neighbor not in visited:
                new_distance = distances[min_station] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = min_station

    return distances, predecessors

# Calculate the unique journey durations and find longest path in reduced network
all_reduced_durations = []
reduced_longest_duration = 0
reduced_longest_paths = []

for start_station in reduced_graph:
    distances, predecessors = dijkstra_shortest_path(reduced_graph, start_station)

    for destination_station, journey_time in distances.items():
        if start_station < destination_station and journey_time != float('inf'):
            all_reduced_durations.append(journey_time)

            if journey_time > reduced_longest_duration:
                reduced_longest_duration = journey_time
                reduced_longest_paths = []

            if journey_time == reduced_longest_duration:
                path = []
                current = destination_station
                while current:
                    path.append(current)
                    current = predecessors[current]
                path.reverse()
                reduced_longest_paths.append((start_station, destination_station, path))

# Plot histogram for longest journey durations in the reduced network
plt.figure(figsize=(10, 5))
plt.hist(all_reduced_durations, bins=100, edgecolor='black')
plt.title("Histogram of Journey Durations on Reduced London Underground Network")
plt.xlabel("Journey Duration (Minutes)")
plt.ylabel("Frequency")
plt.grid(axis='y')
plt.show()

# Display the longest journey details in the reduced network
print(f"\nLongest journey duration in reduced network: {reduced_longest_duration} minutes")
print("Paths for longest journeys in reduced network:")
if reduced_longest_paths:
    for start, end, path in reduced_longest_paths:
        print(f"Starting Station: {start} \nEnding Station: {end} \nPath: {' -> '.join(path)}")
else:
    print("No paths found for the longest duration.")



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
