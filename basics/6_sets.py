# sets
# A set is an unordered collection of zero or more immutable Python data objects
# Sets do not allow duplicates and are written as comma-delimited values enclosed in curly braces
# Sets are heterogeneous, and the collection can be assigned to a variable as below.

s1 = {1, 2, 3, False}
s2 = {3, 4, 5}

s1.union(s2)
s1.difference(s2)
s1.issubset(s2)
s1.clear()

s1.intersection(s2)


s1.add(5)
s1.remove(5)

s1.pop()
