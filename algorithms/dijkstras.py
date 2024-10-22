from collections import defaultdict
import heapq

class Graph:
    def __init__(self):
        # Using defaultdict to automatically initialize empty lists for new vertices
        self.graph = defaultdict(list)
    
    def add_edge(self, u, v, weight):
        # Adding edges for undirected graph
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))
    
    def dijkstra(self, src):
        # Initialize distances dictionary with infinity for all vertices
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[src] = 0
        
        # Priority queue to store vertices and their distances
        # Format: (distance, vertex)
        pq = [(0, src)]
        
        # Set to keep track of visited vertices
        visited = set()
        
        # Dictionary to store the shortest path
        previous = {vertex: None for vertex in self.graph}
        
        while pq:
            # Get vertex with minimum distance
            current_distance, current_vertex = heapq.heappop(pq)
            
            # If we've already processed this vertex, skip it
            if current_vertex in visited:
                continue
                
            visited.add(current_vertex)
            
            # If current_distance is greater than known distance, skip
            if current_distance > distances[current_vertex]:
                continue
            
            # Check all neighbors of the current vertex
            for neighbor, weight in self.graph[current_vertex]:
                if neighbor in visited:
                    continue
                    
                # Calculate new distance to neighbor
                distance = current_distance + weight
                
                # If we found a shorter path, update it
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances, previous
    
    def get_path(self, previous, src, dest):
        """Reconstruct path from source to destination using previous dictionary"""
        path = []
        current = dest
        
        while current is not None:
            path.append(current)
            current = previous[current]
            
        return path[::-1] if path[0] == src else []