import sys
import random
import time
import matplotlib.pyplot as plt

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph  # Graph data structure for adjacency list representation
from dijkstra import dijkstra  # Dijkstra's algorithm for finding the shortest path
from generate_random_graph import generate_random_graph  # Utility to generate random graphs

# Function to generate a random artificial tube network with `n` stations
def generate_random_tube_network(n, max_journey_duration=30):
    """
    Creates a random graph simulating a tube network with specified parameters.

    Args:
        n (int): Number of stations in the network.
        max_journey_duration (int): Maximum weight for the edges representing journey duration.

    Returns:
        tuple: A tuple containing the list of stations, list of edges with weights, and total number of edges.
    """
    graph = generate_random_graph(n, edge_probability=0.1, by_adjacency_lists=True,
                                  directed=False, weighted=True,
                                  min_weight=1, max_weight=max_journey_duration)
    stations = [f"Station_{i}" for i in range(n)]
    edges = []
    edge_count = 0  # Initialize edge count
    for u in range(graph.get_card_V()):
        for edge in graph.get_adj_list(u):
            if u < edge.get_v():  # Ensure each edge is counted once
                edges.append((f"Station_{u}", f"Station_{edge.get_v()}", edge.get_weight()))
                edge_count += 1  # Count each unique edge
    return stations, edges, edge_count

# Function to create an adjacency list graph from given stations and edges
def create_graph(stations, edges):
    """
    Initializes a graph using a list of stations and journey times between them.

    Args:
        stations (list): List of station names.
        edges (list): List of tuples (start, end, weight) representing the journey time between stations.

    Returns:
        tuple: Returns the created graph and a dictionary mapping station names to their indices.
    """
    station_to_index = {station: index for index, station in enumerate(stations)}
    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for station_a, station_b, time in edges:
        u = station_to_index[station_a]
        v = station_to_index[station_b]
        if not graph.has_edge(u, v):
            graph.insert_edge(u, v, time)
    return graph, station_to_index

# Function to measure execution time of finding shortest paths between station pairs
def measure_execution_time(graph, station_to_index, n_tests=10):
    """
    Measures the average time taken to compute shortest paths in the graph.

    Args:
        graph (AdjacencyListGraph): The graph in which to find paths.
        station_to_index (dict): Mapping from station names to indices in the graph.
        n_tests (int): Number of random tests to perform for averaging the execution time.

    Returns:
        float: The average execution time for the given number of tests.
    """
    total_time = 0.0
    stations = list(station_to_index.keys())
    for _ in range(n_tests):
        start_station = random.choice(stations)
        end_station = random.choice(stations)
        start_index = station_to_index[start_station]
        end_index = station_to_index[end_station]
        start_time = time.time()
        dijkstra(graph, start_index)
        total_time += (time.time() - start_time)
    return total_time / n_tests

# Function to run the experiment for different network sizes and plot the results
def run_experiment_and_plot():
    """
    Runs the experiment to measure average execution time for different network sizes,
    and plots the results.
    """
    network_sizes = list(range(100, 1100, 100))
    avg_execution_times = []
    line_section_counts = []  # Store line section counts

    for n in network_sizes:
        print(f"Running experiment for network size: {n} stations")
        stations, edges, edge_count = generate_random_tube_network(n)
        graph, station_to_index = create_graph(stations, edges)
        avg_time = measure_execution_time(graph, station_to_index, n_tests=10)
        avg_execution_times.append(avg_time)
        line_section_counts.append(edge_count)  # Store edge count for plotting

    # Plotting results
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(network_sizes, avg_execution_times, marker='o')
    plt.title("Average Execution Time vs Network Size")
    plt.xlabel("Network Size (Number of Stations)")
    plt.ylabel("Average Execution Time (seconds)")

    plt.subplot(1, 2, 2)
    plt.plot(network_sizes, line_section_counts, marker='o', color='green')
    plt.title("Number of Line Sections vs Network Size")
    plt.xlabel("Network Size (Number of Stations)")
    plt.ylabel("Number of Line Sections")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_experiment_and_plot()



############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
