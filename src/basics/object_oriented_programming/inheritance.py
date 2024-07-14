"""
python object oriented programming
examples for single inheritance
"""


class ParentClass:
    """parent class example"""

    def __init__(self, age):
        self.age = age

    # methods
    def print_age(self):
        """prints"""
        print(f"age is {self.age} years old")


class ChildClassV1(ParentClass):
    """inherits from parent class"""

    pass


class ChildClassV2(ParentClass):
    def __init__(self, age, height):
        super().__init__(age)  # if never call this, self.age does not work
        self.height = height


class ChildClassV3(ParentClass):
    def __init__(self, age, height):
        ParentClass.__init__(self, age)  # same as super().__init__(age)
        self.height = height


class ChildClassV4(ParentClass):
    def __init__(self, age, height):
        self.height = height


if __name__ == "__main__":
    parent = ParentClass(age=10)
    print("printing parent class age")
    parent.print_age()

    child = ChildClassV1(age=10)
    print("printing child class v1")
    child.print_age()

    child2 = ChildClassV2(age=10, height=20)
    child2.print_age()
