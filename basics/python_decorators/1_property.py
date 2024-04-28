"""
Python Decorators

@property decorator for classes

"""


class Circle:
    def __init__(self, radius):
        # underscore used to represent private (shld nt be accessed outside)
        self._radius = radius

    @property
    def radius(self):
        """returns radius
        allows to access method without calling it
        i.e c.radius instead of c.radius()
        """
        print("calling radius")
        return self._radius

    @radius.setter
    def radius(self, value):
        """
        sets radius to a new value
        c.radius = 10 instead of c.radius(10)
        """
        if value < 0:
            print("error, radius needs to be positive")
        else:
            self._radius = value
            print("new value for radius set")

    @radius.deleter
    def radius(self):
        """
        deletes radius
        """
        del self._radius
        print("radius deleted")


c = Circle(5)

print(c.radius)

c.radius = 10
print(c.radius)

del c.radius

print(c.radius)
