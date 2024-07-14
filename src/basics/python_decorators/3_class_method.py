"""
Python Decorators

@classmethod decorator for classes
class level data

use cls instead of self
"""


class Student:
    count = 0
    gpa = 0

    def __init__(self, student_name, gpa):
        self.name = student_name
        self.gpa = gpa
        Student.count += 1
        Student.gpa += gpa

    def get_info(self):
        return f"name = {self.name}, gpa = {self.gpa}"

    @classmethod
    def get_count(cls):
        return f"number of students = {cls.count}"

    @classmethod
    def get_average_gpa(cls):
        return f"average gpa = {cls.gpa / cls.count}"


if __name__ == "__main__":
    student1 = Student("jon", 1.5)
    student2 = Student("dan", 2.5)
    student3 = Student("marry", 3.5)
    student4 = Student("shaun", 3.45)
    student5 = Student("daniel", 4.35)

    print(Student.get_count())
    print(Student.get_average_gpa())
