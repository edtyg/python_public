"""
Python object-oriented programming (OOP)
Basics
"""


class Employee:
    """
    parent class

    Attributes:
        first_name (str): The first name of the employee.
        last_name (str): The last name of the employee.
        email (str): The email address of the employee.
    """

    def __init__(self, first_name: str, last_name: str):
        """
        Initializes an Employee object.

        Args:
            first_name (str): The first name of the employee.
            last_name (str): The last name of the employee.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = f"{self.first_name}.{self.last_name}@company.com"

    def fullname(self):
        """
        Prints the full name of the employee.
        """
        print(f"{self.first_name} {self.last_name}")


class Developer(Employee):
    """
    Represents a developer, a child class of Employee.

    Attributes:
        prog_language (str): The programming language the developer specializes in.
    """

    def __init__(self, first_name: str, last_name: str, prog_language: str):
        """
        Initializes a Developer object

        Args:
            first_name (str): The first name of the developer.
            last_name (str): The last name of the developer.
            prog_language (str): The programming language the developer specializes in.
        """
        super().__init__(first_name, last_name)
        self.prog_language = prog_language

    def programming_language(self):
        """
        Prints the prog language of this dev
        """
        print(self.prog_language)


class Manager(Employee):
    """
    Represents a manager, a subclass of Employee.

    Attributes:
        employees (list): A list of employees managed by the manager.
    """

    def __init__(self, first_name: str, last_name: str, employees=None):
        """
        Initializes a Manager object.

        Args:
            first_name (str): The first name of the manager.
            last_name (str): The last name of the manager.
            employees (list, optional): A list of employees managed by the manager
        """
        super().__init__(first_name, last_name)

        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def show_emps(self):
        """
        prints employees
        """
        print(self.employees)

    def add_emp(self, emp):
        """
        Adds an employee to the manager's list of employees.

        Args:
            emp (Employee): The employee to add.
        """
        if emp not in self.employees:
            self.employees.append(emp)


if __name__ == "__main__":
    employee1 = Employee("ed", "tan")
    employee1.fullname()

    dev1 = Developer("ed2", "tan", "python")
    dev1.fullname()
    dev1.programming_language()

    manager1 = Manager("ed3", "tan", ["ed", "ted"])
    manager1.show_emps()
