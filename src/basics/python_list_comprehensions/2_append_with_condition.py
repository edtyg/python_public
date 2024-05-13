"""
Some Python Comprehensions
"""

### List comprehension ###

# 2) append with condition
even_number = []
for i in range(50):
    if i % 2 == 0:
        even_number.append(i)
print("standard method even numbers")
print(even_number)

# using list comprehension
even_number_comp = [i for i in range(50) if i % 2 == 0]
print("list comprehension method")
print(even_number_comp)
