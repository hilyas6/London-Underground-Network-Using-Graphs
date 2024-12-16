import sys

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')  # Adjust this path to your folder

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph  # Graph data structure
from dijkstra import dijkstra  # Dijkstra's shortest path algorithm
from print_path import print_path  # Importing the print_path function

# List of station names and journey times between them
stations = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [
    ('A', 'B', 4),  # A to B takes 4 minutes
    ('A', 'C', 5),  # A to C takes 5 minutes
    ('B', 'D', 9),  # B to D takes 9 minutes
    ('B', 'C', 11), # B to C takes 11 minutes
    ('B', 'E', 7),  # B to E takes 7 minutes
    ('C', 'E', 3),  # C to E takes 3 minutes
    ('D', 'E', 13), # D to E takes 13 minutes
    ('D', 'F', 2),  # D to F takes 2 minutes
    ('E', 'F', 6)   # E to F takes 6 minutes
]

# Create a mapping from station names to indices
station_to_index = {station: index for index, station in enumerate(stations)}

# Create the graph for journey time in minutes
def create_graph_for_time(stations, edges):
    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for station_a, station_b, time in edges:
        u = station_to_index[station_a]
        v = station_to_index[station_b]
        if not graph.has_edge(u, v):
            graph.insert_edge(u, v, time)
    return graph

# Create the graph for number of stops (each edge weight is 1)
def create_graph_for_stops(stations, edges):
    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for station_a, station_b, _ in edges:  # Ignore time, only count stops
        u = station_to_index[station_a]
        v = station_to_index[station_b]
        if not graph.has_edge(u, v):  # Avoid duplicate edges
            graph.insert_edge(u, v, 1)  # Each edge represents 1 stop
    return graph

# Function to find the shortest path using Dijkstra's algorithm
def find_shortest_path(graph, start_station, end_station):
    start_index = station_to_index[start_station]
    end_index = station_to_index[end_station]

    # Run Dijkstra's algorithm to get distances and predecessors
    distances, predecessors = dijkstra(graph, start_index)

    # Use print_path to reconstruct the shortest path
    path = print_path(predecessors, start_index, end_index, lambda x: stations[x])

    return path, distances[end_index]

# Main function to demonstrate path comparison
def main():
    # Create graph based on journey time in minutes
    graph_time = create_graph_for_time(stations, edges)

    # Create graph based on number of stops
    graph_stops = create_graph_for_stops(stations, edges)

    # Display available stations for user reference
    print("Available stations:", ', '.join(stations))

    # Prompt user to enter start and end stations
    start_station = input("Enter the starting station: ").strip().upper()
    end_station = input("Enter the destination station: ").strip().upper()

    # Validate user input
    if start_station not in station_to_index or end_station not in station_to_index:
        print("Invalid station name. Please enter valid station names from the list: ", stations)
    else:
        # Find shortest path based on journey time in minutes
        path_time, duration_time = find_shortest_path(graph_time, start_station, end_station)
        print(f"Shortest path from {start_station} to {end_station} based on journey time: {' -> '.join(path_time)}")
        print(f"Total journey duration (minutes): {duration_time} minutes")

        # Find shortest path based on number of stops
        path_stops, duration_stops = find_shortest_path(graph_stops, start_station, end_station)
        print(f"Shortest path from {start_station} to {end_station} based on number of stops: {' -> '.join(path_stops)}")
        print(f"Total number of stops: {duration_stops}")

        # Compare paths
        if path_time == path_stops:
            print("The paths based on journey time and number of stops are identical.")
        else:
            print("The paths based on journey time and number of stops are different.")

if __name__ == "__main__":
    main()
