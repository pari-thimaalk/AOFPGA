from collections import deque, defaultdict


def get_all_nodes(graph):
    """Get all nodes in the graph (including those that are only targets)."""
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    return all_nodes


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


def build_reverse_graph(graph):
    """
    Builds a reverse graph where edges point backwards.
    If there's an edge A -> B in original graph, reverse has B -> A.

    Args:
        graph: Original adjacency list

    Returns:
        Reverse adjacency list {node: [nodes that point to it]}
    """
    reverse_graph = defaultdict(list)

    for node, neighbors in graph.items():
        for neighbor in neighbors:
            reverse_graph[neighbor].append(node)

    return reverse_graph


def topological_sort_reverse(graph, end):
    """
    Performs topological sort for nodes that can reach 'end'.
    Returns nodes in reverse topological order (leafs first, roots last).

    Args:
        graph: Original adjacency list
        end: Target node

    Returns:
        Tuple of (list of nodes in order, dict of levels)
    """
    reverse_graph = build_reverse_graph(graph)

    # First, find all nodes that can reach 'end' using BFS on reverse graph
    reachable = set()
    queue = deque([end])
    reachable.add(end)
    levels = {end: 0}

    while queue:
        node = queue.popleft()
        # In reverse graph, predecessors are nodes that point TO current node in original
        for predecessor in reverse_graph.get(node, []):
            if predecessor not in reachable:
                reachable.add(predecessor)
                queue.append(predecessor)
                levels[predecessor] = levels[node] + 1

    print(f"Total reachable nodes from '{end}': {len(reachable)}")

    # Now compute out-degree for reachable nodes (how many of their successors are reachable)
    out_degree = defaultdict(int)
    for node in reachable:
        if node in graph:
            for successor in graph[node]:
                if successor in reachable:
                    out_degree[node] += 1

    # Topological sort: start with nodes that have out-degree 0 (leaf nodes)
    queue = deque([end])  # 'end' has out-degree 0
    topo_order = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)

        # Process predecessors (nodes that point to current node)
        for predecessor in reverse_graph.get(node, []):
            if predecessor in reachable:
                out_degree[predecessor] -= 1
                if out_degree[predecessor] == 0:
                    queue.append(predecessor)

    return topo_order, levels


def bottom_up_count_paths(graph, start, end):
    """
    Counts all paths from start to end using bottom-up dynamic programming.
    Uses topological sorting to ensure each node's DP value is computed
    exactly once, after all its successors have been processed.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node ('you')
        end: Ending node ('out')

    Returns:
        Number of paths from start to end
    """
    # Get topological order starting from 'end'
    topo_order, levels = topological_sort_reverse(graph, end)

    # dp[node] = number of paths from node to 'end'
    dp = defaultdict(int)
    dp[end] = 1  # Base case: 'out' has 1 path to itself

    print(f"Starting bottom-up DP from '{end}'")
    print(f"Processing {len(topo_order)} nodes in topological order\n")

    # Group nodes by level for display
    level_groups = defaultdict(list)
    for node in topo_order:
        level_groups[levels[node]].append(node)

    # Process nodes in topological order
    for node in topo_order:
        if node == end:
            continue  # Skip end node, already set to 1

        # Sum paths through all successors
        if node in graph:
            for successor in graph[node]:
                dp[node] += dp[successor]

    # Print level-by-level results
    for level in sorted(level_groups.keys()):
        nodes = level_groups[level]
        print(f"Level {level}: {len(nodes)} nodes")
        # Print first few nodes as examples
        for node in nodes[:5]:
            print(f"  dp['{node}'] = {dp[node]}")
        if len(nodes) > 5:
            print(f"  ... and {len(nodes) - 5} more nodes")
        print()

    print(f"Total levels processed: {len(level_groups)}")
    print(f"Final answer: dp['{start}'] = {dp[start]}")

    return dp[start]


def main():
    # Read the graph from file
    graph = read_graph('puzzle_input.txt')
    all_nodes = get_all_nodes(graph)

    print("Graph statistics:")
    print(f"Nodes with outgoing edges: {len(graph)}")
    print(f"Total unique nodes: {len(all_nodes)}")
    print(f"'you' has {len(graph.get('you', []))} neighbors: {graph.get('you', [])}")
    print(f"'out' has {len(graph.get('out', []))} neighbors: {graph.get('out', [])}")
    print()

    # Find number of paths from 'you' to 'out' using bottom-up DP
    num_paths = bottom_up_count_paths(graph, 'you', 'out')

    print(f"\n{'='*60}")
    print(f"Number of paths from 'you' to 'out': {num_paths}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()