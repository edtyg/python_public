# -*- coding: utf-8 -*-
"""
Created on Fri May 19 21:48:24 2023

@author: Administrator
"""


class ClassA:
    "example class"

    def __init__(self, name):
        self.name = name


class ClassB:
    "example class"

    def __init__(self, name):
        self.name = name


class CompositeClass:
    """composite of classes"""

    def __init__(self, name_a, name_b):
        self.class_a = ClassA(name_a)
        self.class_b = ClassB(name_b)


if __name__ == "__main__":
    composite = CompositeClass("ed", "edd")
    print(composite.class_a.name)  # Output: ed
    print(composite.class_b.name)  # Output: edd
