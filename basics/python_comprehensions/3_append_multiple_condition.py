"""
Some Python Comprehensions
"""

### List comprehension ###

# 3) append with multiple conditions
# strings that start with a and end in y
options = ["any", "albany", "apple", "world", "hello", ""]
valid_string = []
for i in options:
    if len(i) <= 1:
        continue
    if i[0] != "a":
        continue
    if i[-1] != "y":
        continue
    valid_string.append(i)
print("standard method")
print(valid_string)

# using list comprehension
valid_string = [i for i in options if len(i) >= 2 if i[0] == "a" if i[-1] == "y"]
print("list comprehension method")
print(valid_string)
