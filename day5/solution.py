from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple

def parse_input(data: str) -> Tuple[Dict[int, Set[int]], List[List[int]]]:
    # Parse rules and updates sections
    rules_section, updates_section = data.strip().split('\n\n')
    
    # Parse rules into adjacency list (before -> set of after)
    rules: Dict[int, Set[int]] = defaultdict(set)
    for line in rules_section.strip().split('\n'):
        before, after = map(int, line.split('|'))
        rules[before].add(after)
    
    # Parse updates
    updates = []
    for line in updates_section.strip().split('\n'):
        update = list(map(int, line.strip().split(',')))
        updates.append(update)
    
    return rules, updates

def build_graph_for_update(rules: Dict[int, Set[int]], pages: List[int]) -> Dict[int, Set[int]]:
    """Build a graph containing only rules relevant to the given pages."""
    pages_set = set(pages)
    graph = defaultdict(set)
    
    # Only include rules where both pages are in the update
    for before, afters in rules.items():
        if before in pages_set:
            for after in afters:
                if after in pages_set:
                    graph[before].add(after)
    
    return graph

def has_cycle(graph: Dict[int, Set[int]], pages: List[int]) -> bool:
    """Check if the graph has a cycle using DFS."""
    visited = set()
    path = set()
    
    def dfs(node: int) -> bool:
        if node in path:
            return True  # Found cycle
        if node in visited:
            return False
        
        visited.add(node)
        path.add(node)
        
        for next_node in graph[node]:
            if dfs(next_node):
                return True
        
        path.remove(node)
        return False
    
    # Try starting from each node
    for page in pages:
        if page not in visited:
            if dfs(page):
                return True
    
    return False

def topological_sort(graph: Dict[int, Set[int]], pages: List[int]) -> List[int]:
    """Return topologically sorted list of pages."""
    # Calculate in-degree for each node
    in_degree = defaultdict(int)
    for node in pages:
        for next_node in graph[node]:
            in_degree[next_node] += 1
    
    # Start with nodes that have no dependencies
    queue = deque([page for page in pages if in_degree[page] == 0])
    result = []
    
    # Process nodes in order
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Reduce in-degree of neighbors
        for next_node in graph[node]:
            in_degree[next_node] -= 1
            if in_degree[next_node] == 0:
                queue.append(next_node)
    
    return result

def is_valid_order(sorted_pages: List[int], original_pages: List[int]) -> bool:
    """Check if the original order respects the sorted order."""
    # Build position lookup for original order
    pos = {page: i for i, page in enumerate(original_pages)}
    
    # Check if relative positions match sorted order
    for i in range(len(sorted_pages)):
        for j in range(i + 1, len(sorted_pages)):
            if pos[sorted_pages[i]] > pos[sorted_pages[j]]:
                return False
    
    return True

def solve_part1(data: str) -> int:
    rules, updates = parse_input(data)
    total = 0
    
    for update in updates:
        # Build graph for this update
        graph = build_graph_for_update(rules, update)
        
        # Skip if there's a cycle (impossible to satisfy)
        if has_cycle(graph, update):
            continue
        
        # Get topologically sorted order
        sorted_pages = topological_sort(graph, update)
        
        # Check if original order is valid
        if is_valid_order(sorted_pages, update):
            # Add middle page number
            middle_idx = len(update) // 2
            total += update[middle_idx]
    
    return total

def solve_part2(data: str) -> int:
    rules, updates = parse_input(data)
    total = 0
    
    for update in updates:
        # Build graph for this update
        graph = build_graph_for_update(rules, update)
        
        # Skip if there's a cycle (impossible to satisfy)
        if has_cycle(graph, update):
            continue
        
        # Get topologically sorted order
        sorted_pages = topological_sort(graph, update)
        
        # If original order is NOT valid
        if not is_valid_order(sorted_pages, update):
            # Create mapping from sorted order to original pages
            pos_map = {page: i for i, page in enumerate(sorted_pages)}
            
            # Sort the original pages according to the topological order
            sorted_update = sorted(update, key=lambda x: pos_map[x])
            
            # Add middle page number
            middle_idx = len(sorted_update) // 2
            total += sorted_update[middle_idx]
    
    return total

if __name__ == "__main__":
    # Test with sample input first
    sample_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    print("Testing with sample input...")
    result = solve_part1(sample_input)
    print(f"Test result part 1: {result}")
    assert result == 143, f"Test failed! Expected 143, got {result}"

    result = solve_part2(sample_input)
    print(f"Test result part 2: {result}")
    assert result == 123, f"Test failed! Expected 123, got {result}"

    # Now try real input
    print("\nSolving with real input...")
    with open("input") as f:
        data = f.read()
    result = solve_part1(data)
    print(f"Part 1 result: {result}")
    
    result = solve_part2(data)
    print(f"Part 2 result: {result}")
