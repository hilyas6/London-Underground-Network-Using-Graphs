import sys
import pandas as pd
import matplotlib.pyplot as plt

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph # Graph data structure for adjacency list representation
from dijkstra import dijkstra  # Import Dijkstra's algorithm for finding the shortest path
from print_path import print_path # Import the print_path function for getting journey path

# Load the London Underground data
file_path = 'London Underground Data.xlsx'  #File name in PyCharm directory of data
underground_data = pd.read_excel(file_path, usecols=[0, 1, 2, 3], names=["Line", "Station1", "Station2", "JourneyTime"])

# Filter rows where both 'Station2' and 'JourneyTime' are filled, indicating direct connections with journey times
connections_data = underground_data.dropna(subset=["Station2", "JourneyTime"])
connections_data = connections_data[connections_data["Station1"] != connections_data["Station2"]]

# Create the adjacency list graph using AdjacencyListGraph from the library
graph = AdjacencyListGraph(len(set(connections_data["Station1"]).union(set(connections_data["Station2"]))), directed=False, weighted=True)

# Mapping stations to indices
station_to_index = {}
index_to_station = []
index = 0

# Adding edges to the graph and building the station mapping
for _, row in connections_data.iterrows():
    station1 = row["Station1"]
    station2 = row["Station2"]
    journey_time = row["JourneyTime"]

    if station1 not in station_to_index:
        station_to_index[station1] = index
        index_to_station.append(station1)
        index += 1

    if station2 not in station_to_index:
        station_to_index[station2] = index
        index_to_station.append(station2)
        index += 1

    u = station_to_index[station1]
    v = station_to_index[station2]

    if not graph.has_edge(u, v):
        graph.insert_edge(u, v, journey_time)

# Calculate all unique pairwise shortest paths and track the longest journeys
all_durations = []  # List to store unique journey durations for histogram
total_journey_calculations = 0  # Counter for the total number of journey duration calculations
longest_duration = 0
longest_paths = set()

for start_station in station_to_index:
    start_index = station_to_index[start_station]
    distances, predecessors = dijkstra(graph, start_index)

    for destination_station, destination_index in station_to_index.items():
        if start_index < destination_index and distances[destination_index] < float('inf'):
            all_durations.append(distances[destination_index])
            total_journey_calculations += 1
            if distances[destination_index] > longest_duration:
                longest_duration = distances[destination_index]
                longest_paths.clear()
            if distances[destination_index] == longest_duration:
                path = tuple(print_path(predecessors, start_index, destination_index, lambda x: index_to_station[x]))
                longest_paths.add((index_to_station[start_index], index_to_station[destination_index], path))

# Histogram of journey durations
plt.figure(figsize=(10, 5))
plt.hist(all_durations, bins=100, edgecolor='black')
plt.title("Histogram of Unique Journey Durations on the London Underground")
plt.xlabel("Journey Duration (Minutes)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# Print the longest journey details, distinguishing the two longest paths if they exist
print(f"\nLongest journey duration: {longest_duration} minutes")
print("Total number of journey durations calculated:", total_journey_calculations)
if len(longest_paths) == 1:
    print("There is only one path with the longest journey duration:")
else:
    print(f"There are {len(longest_paths)} paths with the longest journey duration:")

for i, (start, end, path) in enumerate(longest_paths, start=1):
    print(f"\nPath of Longest Journey {i}:")
    print(f"Starting Station: {start} \nEnding Station: {end} \nPath: {' -> '.join(path)}")



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
