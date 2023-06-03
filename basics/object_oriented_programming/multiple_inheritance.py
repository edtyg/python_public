class ParentClass1:
    def __init__(self, attr1):
        self.attr1 = attr1

    def method1(self):
        print("Method 1 from ParentClass1")


class ParentClass2:
    def __init__(self, attr2):
        self.attr2 = attr2

    def method2(self):
        print("Method 2 from ParentClass2")


class ChildClass(ParentClass1, ParentClass2):
    def __init__(self, attr1, attr2, attr3):
        ParentClass1.__init__(self, attr1)
        ParentClass2.__init__(self, attr2)
        self.attr3 = attr3


child = ChildClass("Value 1", "Value 2", "Value 3")
print(child.attr1)  # Output: Value 1
print(child.attr2)  # Output: Value 2
print(child.attr3)  # Output: Value 3
child.method1()  # Output: Method 1 from ParentClass1
child.method2()  # Output: Method 2 from ParentClass2
