import sys
import random
import time
import matplotlib.pyplot as plt

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph  # Graph data structure for adjacency list representation
from dijkstra import dijkstra  # Import Dijkstra's algorithm for finding the shortest path
from generate_random_graph import generate_random_graph  # Import generate_random_graph for generating randon graphs

# Function to generate an artificial tube network with n stations, using stops as the metric
def generate_random_tube_network(n):
    graph = generate_random_graph(n, edge_probability=0.1, by_adjacency_lists=True, directed=False, weighted=True)
    stations = [f"Station_{i}" for i in range(n)]
    edges = []
    # Iterate through each vertex to access its adjacency list
    for u in range(graph.get_card_V()):
        for edge in graph.get_adj_list(u):
            if u < edge.get_v():  # Ensure each edge is counted only once
                edges.append((f"Station_{u}", f"Station_{edge.get_v()}", 1))  # Weight set to 1 for each stop

    return stations, edges, len(edges)  # Return the number of edges

# Function to create the graph from the stations and edges
def create_graph(stations, edges):
    station_to_index = {station: index for index, station in enumerate(stations)}
    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for station_a, station_b, stops in edges:
        u = station_to_index[station_a]
        v = station_to_index[station_b]
         # Insert each edge into the graph if it does not already exist
        if not graph.has_edge(u, v):
            graph.insert_edge(u, v, stops)

    return graph, station_to_index

# Function to measure the execution time of Dijkstra's algorithm across multiple tests for a given graph
def measure_execution_time(graph, station_to_index, n_tests=10):
    total_time = 0.0
    stations = list(station_to_index.keys())
    # Execute Dijkstra's algorithm multiple times and record the execution time
    for _ in range(n_tests):
        start_station = random.choice(stations)
        end_station = random.choice(stations)
        start_index = station_to_index[start_station]
        end_index = station_to_index[end_station]
        start_time = time.time()
        dijkstra(graph, start_index)
        total_time += (time.time() - start_time)

    return total_time / n_tests

# Function to run the experiment for various network sizes and plot the results
def run_experiment_and_plot():
    network_sizes = list(range(1100, 2100, 100))  # Network Sizes: 1100, 1200, ..., 2000
    avg_execution_times = []
    line_section_counts = []

    for n in network_sizes:
        print(f"Running experiment for network size: {n} stations")

        # Generate random tube network with n stations
        stations, edges, line_sections = generate_random_tube_network(n)

        # Create the graph
        graph, station_to_index = create_graph(stations, edges)

        # Measure average execution time for n-tests
        avg_time = measure_execution_time(graph, station_to_index, n_tests=10)
        avg_execution_times.append(avg_time)

        # Keep track of the line section counts
        line_section_counts.append(line_sections)

    # Plotting execution times
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(network_sizes, avg_execution_times, marker='o')
    plt.title("Average Execution Time vs Network Size")
    plt.xlabel("Network Size (Number of Stations)")
    plt.ylabel("Average Execution Time (seconds)")

    # Plotting line sections
    plt.subplot(1, 2, 2)
    plt.plot(network_sizes, line_section_counts, marker='o', color='green')
    plt.title("Number of Line Sections vs Network Size")
    plt.xlabel("Network Size (Number of Stations)")
    plt.ylabel("Number of Line Sections")

    plt.tight_layout()
    plt.show()

# Run the experiment
if __name__ == "__main__":
    run_experiment_and_plot()



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
