import argparse
import math
import time
from heapq import heappop, heappush


# Read the network topology from a file
def read_network_topology(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()

    num_nodes = int(lines[0].strip())  # First line is the number of nodes
    graph = [
        [math.inf] * num_nodes for _ in range(num_nodes)
    ]  # Initialize graph with infinity

    for line in lines[1:]:
        n1, n2, cost = line.split()
        n1, n2 = int(n1), int(n2)
        cost = float(cost)

        graph[n1][n2] = cost
        graph[n2][n1] = cost  # Since it's a bidirectional link

    return num_nodes, graph


def distance_vector_routing(graph, num_nodes, source_node):
    D = [math.inf] * num_nodes
    D[source_node] = 0
    paths = {source_node: [source_node]}

    for _ in range(num_nodes - 1):
        updated = False
        for u in range(num_nodes):
            for v in range(num_nodes):
                if graph[u][v] != math.inf and D[u] + graph[u][v] < D[v]:
                    D[v] = D[u] + graph[u][v]
                    paths[v] = paths[u] + [v]
                    updated = True

        if not updated:
            break

    return D, paths


def dijkstra_algorithm(graph, num_nodes, source_node):
    D = [math.inf] * num_nodes
    D[source_node] = 0
    paths = {source_node: [source_node]}
    pq = [(0, source_node)]  # Priority queue with (cost, node)

    while pq:
        current_dist, u = heappop(pq)

        if current_dist > D[u]:
            continue

        for v in range(num_nodes):
            if graph[u][v] != math.inf:
                dist = current_dist + graph[u][v]
                if dist < D[v]:
                    D[v] = dist
                    paths[v] = paths[u] + [v]
                    heappush(pq, (dist, v))

    return D, paths


def path_vector_routing(graph, num_nodes, source_node):
    D = [math.inf] * num_nodes
    D[source_node] = 0
    paths = {source_node: [source_node]}

    for _ in range(num_nodes - 1):
        updated = False
        for u in range(num_nodes):
            for v in range(num_nodes):
                if graph[u][v] != math.inf and D[u] + graph[u][v] < D[v]:
                    D[v] = D[u] + graph[u][v]
                    paths[v] = paths[u] + [v]
                    updated = True

        if not updated:
            break

    return D, paths


def print_results(algorithm_name, distances, paths, num_nodes, start_time):
    print(f"{algorithm_name}:")
    for i in range(num_nodes):
        if i != 0:  # Don't print path to itself
            path = "->".join(map(str, paths[i]))
            print(f"Shortest path to node {i} is {path} with cost {distances[i]}")
    end_time = time.time()
    print(f"Time Elapsed: {end_time - start_time} seconds\n")


def main():
    # Running all algorithms and outputting results
    start_time = time.time()
    distances, paths = distance_vector_routing(graph, num_nodes, source_node)
    print_results("Distance Vector Routing", distances, paths, num_nodes, start_time)

    start_time = time.time()
    distances, paths = dijkstra_algorithm(graph, num_nodes, source_node)
    print_results("Dijkstra's Algorithm", distances, paths, num_nodes, start_time)

    start_time = time.time()
    distances, paths = path_vector_routing(graph, num_nodes, source_node)
    print_results("Path Vector Routing", distances, paths, num_nodes, start_time)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script runs 3 algorithms to calculate the shortest routing distance"
    )
    parser.add_argument("filename", help="The name of the file to process.")
    parser.add_argument("sourcenode", help="The source node that we start with.")

    args = parser.parse_args()

    num_nodes, graph = read_network_topology(args.filename)
    source_node = int(args.sourcenode)

    main()
