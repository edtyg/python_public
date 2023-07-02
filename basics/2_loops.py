"""
examples for writing loops
for loops, while loops
"""

# this prints 1 to 9, step 2
for i in range(1, 10, 2):
    print(i)

for i in range(10):
    # 0 to 9
    print(i)

# while loop
i = 0
while i < 10:
    print(i)
    i = i + 1


# if else statements
def testing(x):
    if x == 1:
        return x + 4
    elif x == 2:
        return x + 3
    else:
        return x + 100


fruits = ["apple", "banana", "watermelon"]

# enumerate saves the index
for count, items in enumerate(fruits):
    print(count, items)
