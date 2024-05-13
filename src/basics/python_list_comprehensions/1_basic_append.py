"""
Some Python Comprehensions
"""

### List comprehension ###

# standard append
values = []
for i in range(10):
    values.append(i)
print("standard method")
print(values)

# using list comprehension
values_comp = [i for i in range(10)]
print("list comprehension method")
print(values_comp)
