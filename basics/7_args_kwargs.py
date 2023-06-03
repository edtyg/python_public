# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 15:59:08 2022

@author: Edgar Tan
"""


# args unpacking operator is a tuple
def sum_values(*args: list):
    # returns sum of the values in multiple lists
    empty = []
    for list_of_numbers in args:
        for j in list_of_numbers:
            empty.append(j)

    return sum(empty)


# kwargs unpacking operator is a dictionary
def sum_values_v2(**kwargs: dict):
    empty = []
    for i in kwargs.keys():
        empty.append(kwargs[i])

    return sum(empty)


if __name__ == "__main__":
    v = sum_values([1, 2, 3], [4, 5, 6])
    print(v)

    d = {"a": 1, "b": 3, "c": 5}
    v2 = sum_values_v2(**d)
    print(v2)
