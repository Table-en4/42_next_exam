Write a function island_matrix_counter(matrix) that receives a 2D matrix containing "1" and "0" string values and returns the total number of islands.

An island is a group of connected "1" cells. Cells are considered connected only when they are directly adjacent horizontally (left, right) or vertically (up, down). Diagonal cells do not count as connected.

Requirements:
- "1" represents land.
- "0" represents water.
- Count each separate island exactly once.
- An empty matrix (or matrix with no rows) should return 0.
- DFS/BFS traversal or matrix mutation can be used to explore each complete island.