"""
tuples are ordered, immutable collection of elements
cannot be modified once created
have to create a new tuple if any
"""

t = ()
type(t)

words_tuple = ("sword", "shield", "sword")
print(words_tuple)

numbers_tuple = (9, 9, 8, 7, 7, 1, 22, 33, 123, 5, 5, 5, 5)
print(numbers_tuple)

for word in words_tuple:
    print(word)

# indexing of tuples
t[0]
t[1]
t[-1]


### some tuple methods
numbers_tuple.count(5)  # count number of times value occurs in the tuple
numbers_tuple.index(5)  # find the index of the first instance of value

length = len(numbers_tuple)
print(f"length of tuple = {length}")

# sorts tuple
sorted_tuple = sorted(numbers_tuple)  # returns a sorted list - original tuple unchanged

tuple_from_list = tuple(sorted_tuple)  # creates a tuple from a list
