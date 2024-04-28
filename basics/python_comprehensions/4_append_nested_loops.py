"""
Some Python Comprehensions
"""

### List comprehension ###

# 4) nested loops
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = []
for lst in matrix:
    for val in lst:
        flattened.append(val)
print("standard method")
print(flattened)

# using list comprehension
flattened = [x for lst in matrix for x in lst]
print("list comprehension method")
print(flattened)
