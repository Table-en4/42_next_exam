Write a function that maps a constellation of stars onto a grid and returns the visual representation as a list of strings.

The function should:
- Take a list of star coordinates as tuples (row, col) and grid size as integer
- Return a list of strings representing the grid
- Stars are represented by '*' and empty spaces by '.'
- Grid coordinates start from (0, 0) at top-left
- Ignore coordinates outside the grid boundaries
- Handle duplicate coordinates (star appears only once)