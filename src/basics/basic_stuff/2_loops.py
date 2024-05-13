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

[print(x) for x in range(10)]
[x for x in range(10)]

# while loop
i = 0
while i < 10:
    print(i)
    i = i + 1


# if else statements
def testing(x):
    """_summary_

    Args:
        x (_type_): _description_

    Returns:
        _type_: _description_
    """
    if x == 1:
        return x + 4
    elif x == 2:
        return x + 3
    else:
        return x + 100


fruits = ["apple", "banana", "watermelon", "durian"]

# enumerate saves the index
for list_index, items in enumerate(fruits):
    print(list_index, items)

data_dict = {1: "a", 2: "b", 3: "c"}
for key, value in data_dict.items():
    print(key, value)
