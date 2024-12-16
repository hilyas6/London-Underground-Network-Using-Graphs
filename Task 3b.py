import pandas as pd
import matplotlib.pyplot as plt
import sys

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph # Graph data structure for adjacency list representation
from dijkstra import dijkstra # Import Dijkstra's algorithm for finding the shortest path
from print_path import print_path # Import the print_path function for getting journey path

# Load the London Underground data
file_path = 'London Underground Data.xlsx' #File name in PyCharm directory of data
underground_data = pd.read_excel(file_path, usecols=[0, 1, 2, 3], names=["Line", "Station1", "Station2", "JourneyTime"])

# Filter rows where both 'Station2' and 'JourneyTime' are filled, indicating direct connections with journey times
connections_data = underground_data.dropna(subset=["Station2", "JourneyTime"])
connections_data = connections_data[connections_data["Station1"] != connections_data["Station2"]]

# Create an adjacency list graph for stops
stations = list(set(connections_data["Station1"]).union(connections_data["Station2"]))
station_to_index = {station: idx for idx, station in enumerate(stations)}
graph_stops = AdjacencyListGraph(len(station_to_index), directed=False, weighted=True)

# Populate the graph with edges, each edge represents 1 stop
for _, row in connections_data.iterrows():
    u = station_to_index[row["Station1"]]
    v = station_to_index[row["Station2"]]
    if not graph_stops.has_edge(u, v):
        graph_stops.insert_edge(u, v, 1)

# Calculate all unique pairwise shortest paths in terms of number of stops
number_of_stops = []
total_journey_calculations = 0  # Counter for the total number of journey duration calculations
longest_stops = 0
longest_path = []
start_station_index = end_station_index = None

for start_index in range(len(station_to_index)):
    distances, predecessors = dijkstra(graph_stops, start_index)
    for end_index in range(len(station_to_index)):
        if end_index != start_index and distances[end_index] < float('inf'):  # Valid path found
            number_of_stops.append(distances[end_index])
            total_journey_calculations += 1
            if distances[end_index] > longest_stops:
                longest_stops = distances[end_index]
                start_station_index = start_index
                end_station_index = end_index
                path = print_path(predecessors, start_index, end_index, lambda x: stations[x])
                longest_path = path

# Plot histogram of the number of stops
plt.figure(figsize=(10, 5))
plt.hist(number_of_stops, bins=50, edgecolor='black')
plt.title("Histogram of Number of Stops on London Underground")
plt.xlabel("Number of Stops")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# Print the longest journey details in terms of stops
starting_station = stations[start_station_index]
ending_station = stations[end_station_index]
print(f"Longest path in terms of number of stops: {longest_stops} stops")
print(f"Starting Station: {starting_station} \nEnding Station: {ending_station}")
print(f"Path: {' -> '.join(longest_path)}")
print("Total number of journey durations calculated:", total_journey_calculations)



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
