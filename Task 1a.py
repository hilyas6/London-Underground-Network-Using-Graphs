import sys

# Setting up the path to include the folder where the library codes are stored
sys.path.append('/Users/hamzaalikhan/PycharmProjects/Advanced ADS Coursework/Book library code')

# Import necessary modules/code library from the book library code folder
from adjacency_list_graph import AdjacencyListGraph  # Graph data structure for adjacency list representation
from dijkstra import dijkstra  # Dijkstra's algorithm for finding the shortest path
from print_path import print_path  # Import the print_path function for getting journey path

# List of station names and journey times between them.
stations = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [ ('A', 'B', 4), ('A', 'C', 5), ('B', 'D', 9), ('B', 'C', 11), ('B', 'E', 7), ('C', 'E', 3), ('D', 'E', 13), ('D', 'F', 2), ('E', 'F', 6) ]

# Mapping station names to indices to facilitate graph operations
station_to_index = {station: index for index, station in enumerate(stations)}

# Creating the graph from the list of stations and journey times
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)
for station_a, station_b, time in edges:
    u = station_to_index[station_a]
    v = station_to_index[station_b]
    if not graph.has_edge(u, v):  # Adding each edge only if it does not exist to avoid duplicates
        graph.insert_edge(u, v, time)

# Function to find the shortest path and journey duration between two stations using Dijkstra's algorithm
def find_shortest_path(graph, start_station, end_station):
    start_index = station_to_index[start_station]
    end_index = station_to_index[end_station]
    distances, predecessors = dijkstra(graph, start_index)  # Run Dijkstra's algorithm

    # Use print_path to get the shortest path
    path = print_path(predecessors, start_index, end_index, lambda x: stations[x])
    return path, distances[end_index]

# Main function to interact with the user
def main():
    print("Available stations:", ', '.join(stations))
    start_station = input("Enter the starting station: ").strip().upper()
    end_station = input("Enter the destination station: ").strip().upper()

    if start_station not in station_to_index or end_station not in station_to_index:
        print("Invalid station name. Please enter valid station names from the list: ", stations)
    else:
        path, duration = find_shortest_path(graph, start_station, end_station)
        if path is None:
            print("No path found.")
        else:
            print(f"The shortest path from {start_station} to {end_station} is: {' -> '.join(path)}")
            print(f"Total journey duration: {duration} minutes")

if __name__ == "__main__":
    main()


############################ REFERENCES #################################
#   1.	Introduction to Algorithms, Fourth edition, by Thomas H. Cormen,
#       Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein.
#   2.	Lecture slides from week 1 to week 6
#   3.	Youtube, Google & OpenAI were used for getting ideas
#########################################################################
