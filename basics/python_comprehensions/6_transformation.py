"""
Some Python Comprehensions
"""

### List comprehension ###


def square(value: float):
    """
    returns the square of a value
    """
    return value * value


squared_numbers = [square(x) for x in range(10)]
print(squared_numbers)
