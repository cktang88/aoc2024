from collections import defaultdict, deque
import random

def read_input(filename="input"):
    with open(filename, "r") as f:
        return f.read().strip()

def parse_graph(data):
    """Parse input into adjacency list"""
    graph = defaultdict(set)
    edges = set()
    
    for line in data.splitlines():
        source, targets = line.split(": ")
        for target in targets.split():
            graph[source].add(target)
            graph[target].add(source)
            edges.add(tuple(sorted([source, target])))
    
    return graph, edges

def bfs_path(graph, start, end, excluded_edges=None):
    """Find a path between start and end avoiding excluded edges"""
    if excluded_edges is None:
        excluded_edges = set()
        
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        vertex, path = queue.popleft()
        for next_vertex in graph[vertex]:
            if next_vertex not in visited and tuple(sorted([vertex, next_vertex])) not in excluded_edges:
                if next_vertex == end:
                    return path + [next_vertex]
                visited.add(next_vertex)
                queue.append((next_vertex, path + [next_vertex]))
    return None

def find_all_paths(graph, start, end, max_paths=100):
    """Find multiple paths between start and end"""
    paths = []
    excluded_edges = set()
    
    for _ in range(max_paths):
        path = bfs_path(graph, start, end, excluded_edges)
        if not path:
            break
            
        paths.append(path)
        # Add edges from this path to excluded edges to find different paths
        for i in range(len(path) - 1):
            excluded_edges.add(tuple(sorted([path[i], path[i + 1]])))
    
    return paths

def get_edge_frequency(graph):
    """Find how frequently each edge appears in paths between random pairs"""
    edge_count = defaultdict(int)
    vertices = list(graph.keys())
    pairs_to_try = min(len(vertices) * 2, 100)  # Limit number of pairs to try
    
    for _ in range(pairs_to_try):
        start = random.choice(vertices)
        end = random.choice(vertices)
        if start == end:
            continue
            
        paths = find_all_paths(graph, start, end, max_paths=5)  # Limit paths per pair
        for path in paths:
            for i in range(len(path) - 1):
                edge = tuple(sorted([path[i], path[i + 1]]))
                edge_count[edge] += 1
                
    return edge_count

def check_partition(graph, cut_edges):
    """Check if removing these edges creates exactly two components"""
    if len(cut_edges) != 3:
        return None
        
    # Start from any vertex
    start = next(iter(graph))
    visited = {start}
    queue = deque([start])
    
    # Find first component
    while queue:
        vertex = queue.popleft()
        for next_vertex in graph[vertex]:
            edge = tuple(sorted([vertex, next_vertex]))
            if edge not in cut_edges and next_vertex not in visited:
                visited.add(next_vertex)
                queue.append(next_vertex)
    
    # If we visited all vertices, not a valid cut
    if len(visited) == len(graph):
        return None
        
    # Return size of both components
    return len(visited) * (len(graph) - len(visited))

def solve_part1(data):
    graph, edges = parse_graph(data)
    
    # Find edges that appear most frequently in paths
    edge_freq = get_edge_frequency(graph)
    
    # Sort edges by frequency, highest first
    sorted_edges = sorted(edge_freq.items(), key=lambda x: (-x[1], x[0]))
    
    # Try combinations of the most frequent edges
    top_edges = [edge for edge, _ in sorted_edges[:10]]  # Only try top 10 most frequent edges
    
    for i in range(len(top_edges)-2):
        for j in range(i+1, len(top_edges)-1):
            for k in range(j+1, len(top_edges)):
                cut = {top_edges[i], top_edges[j], top_edges[k]}
                result = check_partition(graph, cut)
                if result:
                    return result
    
    return None

def main():
    # Test with example input
    test_input = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    
    print("Testing with example input...")
    result = solve_part1(test_input)
    print(f"Test result: {result}")
    assert result == 54, f"Test failed! Expected 54, got {result}"
    print("Test passed!")
    
    print("\nSolving with real input...")
    data = read_input()
    result = solve_part1(data)
    print(f"Part 1: {result}")

if __name__ == "__main__":
    main()
