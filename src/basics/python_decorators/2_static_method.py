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


class Mathv2:

    def add(self, x, y):
        return x + y

    def multiply(self, x, y):
        return x * y


if __name__ == "__main__":

    # z = Math()
    # print(z)
    # y = z.add(1, 2)
    # print(y)

    # y = Mathv2()
    # print(y)
    # z = y.add(1, 2)
    # print(z)
