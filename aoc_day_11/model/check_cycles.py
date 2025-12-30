def read_graph(filename):
    """Read graph from file."""
    adjacency_list = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            source = parts[0].strip()
            targets = parts[1].strip().split()
            if source not in adjacency_list:
                adjacency_list[source] = []
            adjacency_list[source].extend(targets)
    return adjacency_list


def find_cycle_dfs(graph, node, visited, rec_stack, path):
    """
    DFS to find a cycle in the graph.

    Args:
        graph: Adjacency list
        node: Current node
        visited: Set of all visited nodes
        rec_stack: Recursion stack for current path
        path: Current path taken

    Returns:
        List representing a cycle if found, None otherwise
    """
    visited.add(node)
    rec_stack.add(node)
    path.append(node)

    if node in graph:
        for neighbor in graph[node]:
            if neighbor not in visited:
                result = find_cycle_dfs(graph, neighbor, visited, rec_stack, path)
                if result:
                    return result
            elif neighbor in rec_stack:
                # Found a cycle! Return the cycle path
                cycle_start_idx = path.index(neighbor)
                return path[cycle_start_idx:] + [neighbor]

    path.pop()
    rec_stack.remove(node)
    return None


def find_cycles(graph):
    """Find all cycles in the graph."""
    visited = set()
    cycles = []

    for node in graph:
        if node not in visited:
            rec_stack = set()
            path = []
            cycle = find_cycle_dfs(graph, node, visited, rec_stack, path)
            if cycle:
                cycles.append(cycle)
                print(f"Found cycle: {' -> '.join(cycle)}")
                return cycles  # Return after finding first cycle

    return cycles


def main():
    graph = read_graph('puzzle_input.txt')

    print(f"Graph has {len(graph)} nodes")
    print(f"\nSearching for cycles...\n")

    cycles = find_cycles(graph)

    if cycles:
        print(f"\n✓ Graph HAS cycles!")
        print(f"Found {len(cycles)} cycle(s)")
        print(f"\nFirst cycle found:")
        cycle = cycles[0]
        print(f"  {' -> '.join(cycle)}")
        print(f"  Cycle length: {len(cycle) - 1}")
    else:
        print("\n✗ Graph is a DAG (no cycles found)")


if __name__ == '__main__':
    main()