"""
Python Decorators

@staticmethod decorator for classes
something that belongs to the class, and not to an instance of the class

so do not need to initialize it - can call it directly
"""


class Math:

    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def multiply(x, y):
        return x * y


print(Math.add(1, 2))
