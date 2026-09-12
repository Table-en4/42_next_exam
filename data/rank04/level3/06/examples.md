Input
package_dependency_resolver({"app": ["database"], "database": ["driver"], "driver": []})
Output
["driver", "database", "app"]
Input
package_dependency_resolver({"A": [], "B": ["A"], "C": ["A", "B"]})
Output
["A", "B", "C"]
Input
package_dependency_resolver({})
Output
[]
Input
package_dependency_resolver({"X": ["Y"], "Y": ["X"]})
Output
[]
Input
package_dependency_resolver({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]})
Output
["api", "web", "backend", "frontend"]