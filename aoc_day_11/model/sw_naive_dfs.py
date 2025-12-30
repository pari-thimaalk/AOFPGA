def read_graph(filename):
    """
    Reads the graph from a file and constructs an adjacency list.

    Args:
        filename: Path to the input file

    Returns:
        Dictionary representing adjacency list {node: [neighbors]}
    """
    adjacency_list = {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split by colon to get source and targets
            parts = line.split(':')
            source = parts[0].strip()

            # Split targets by space
            targets = parts[1].strip().split()

            # Add edges to adjacency list
            if source not in adjacency_list:
                adjacency_list[source] = []
            adjacency_list[source].extend(targets)

    return adjacency_list


def dfs_count_paths(graph, start, end, visited=None):
    """
    Counts all paths from start to end using DFS.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Ending node
        visited: Set of visited nodes in current path

    Returns:
        Number of paths from start to end
    """
    if visited is None:
        visited = set()

    # Base case: reached the destination
    if start == end:
        return 1

    # If node not in graph or already visited in current path, return 0
    if start not in graph or start in visited:
        return 0

    # Mark current node as visited
    visited.add(start)

    # Count paths through all neighbors
    path_count = 0
    for neighbor in graph[start]:
        path_count += dfs_count_paths(graph, neighbor, end, visited)

    # Backtrack: remove current node from visited
    visited.remove(start)

    return path_count


def main():
    # Read the graph from file
    graph = read_graph('puzzle_input.txt')

    # Find number of paths from 'you' to 'out'
    num_paths = dfs_count_paths(graph, 'you', 'out')

    print(f"Number of paths from 'you' to 'out': {num_paths}")

    # Print some debug info
    print(f"\nGraph statistics:")
    print(f"Total nodes: {len(graph)}")
    print(f"'you' has {len(graph.get('you', []))} neighbors: {graph.get('you', [])}")

    # Check if 'out' is reachable
    out_neighbors = graph.get('out', [])
    if len(out_neighbors) == 0:
        print("'out' is a terminal node (no outgoing edges)")


if __name__ == '__main__':
    main()