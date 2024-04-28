"""
Some Python Comprehensions
"""

### List comprehension ###
categories = []

for i in range(10):
    if i % 2 == 0:
        categories.append("Even")
    else:
        categories.append("Odd")
print("standard method")
print(categories)

categories = ["Even" if x % 2 == 0 else "Odd" for x in range(10)]
print("list comprehension method")
print(categories)
