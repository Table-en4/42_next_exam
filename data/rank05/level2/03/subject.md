Write a function that determines whether a directed graph contains at least one cycle.

The function takes a dictionary representing an adjacency list where keys are integer node IDs and values are lists of integer neighbor node IDs.

The function should:
- Return True if the directed graph contains a cycle.
- Return False if the graph is acyclic or if the input graph dictionary is empty.
- Correctly handle graphs with multiple disconnected components.