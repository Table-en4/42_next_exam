Write a function that determines a valid package installation order by resolving dependencies. Use topological sorting to ensure dependencies are installed before the packages that require them.

The function should:
- Take a dictionary where keys are package names and values are lists of dependencies
- Return packages in installation order (dependencies first)
- Return empty list if no valid order exists (circular dependencies)
- Handle empty input and isolated dependency chains
- Ignore references to packages not in the input dictionary