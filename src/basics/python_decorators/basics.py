"""
Python Decorators

a decorator is a function that modifies another function
"""

import time


def timer(func):
    """
    Decorator function - timer
    """

    # wrapper function acceps any function and returns time taken
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"function took {elapsed_time} seconds")
        return result

    return wrapper


@timer
def summing_up(n):
    x = 0
    for i in range(n):
        x += i
        print(x)


summing_up(1002)
