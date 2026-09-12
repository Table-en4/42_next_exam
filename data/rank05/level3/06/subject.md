Write a function that searches for all occurrences of a target word pattern within a 2D grid of characters in all 8 cardinal and diagonal directions.

The directions and their codes are:
- (1, 0) -> "H" (Horizontal right)
- (-1, 0) -> "H-" (Horizontal left)
- (0, 1) -> "V" (Vertical down)
- (0, -1) -> "V-" (Vertical up)
- (1, 1) -> "D1" (Diagonal down-right)
- (-1, -1) -> "D1-" (Diagonal up-left)
- (-1, 1) -> "D2" (Diagonal up-right)
- (1, -1) -> "D2-" (Diagonal down-left)

The function should:
- Take a grid of strings `grid` and a target string `pattern`.
- Return a list of tuples `(x, y, direction_code)` for each match, where `x` is the column index and `y` is the row index of the first character.
- Return an empty list `[]` if either `grid` or `pattern` is empty.