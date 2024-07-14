"""
If 2 subclass have the same method name
can call them separately

else method from ClassA gets called first
"""


class ClassA:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def print_name(self):
        """prints first name"""
        print(f"name = {self.first_name}")


class ClassB:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def print_name(self):
        """prints last name"""
        print(f"name = {self.last_name}")


class combined(ClassA, ClassB):
    def __init__(self, first_name: str, last_name: str):
        ClassA.__init__(self, first_name, last_name)
        ClassB.__init__(self, first_name, last_name)

    def test(self):
        ClassA.print_name(self)
        ClassB.print_name(self)
        self.print_name()


if __name__ == "__main__":

    first_name = "Steve"
    last_name = "Jobs"

    instance = combined(first_name, last_name)

    instance.test()
