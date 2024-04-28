"""
exception handling
starts with try -> requires except or finally clause

some common types of errors

ZeroDivisionError
ValueError
TypeError
NameError
FileNotFoundError
IndexError
KeyError
AttributeError
ImportError
RuntimeError
"""

try:
    # code that might raise exception here
    z = 10 / a

except ZeroDivisionError:
    # handling exception here
    print("Cannot divide by zero!")

except TypeError:
    print("type error")

except NameError:
    print("check your variable name")

except (TypeError, NameError):
    print("lol")

except Exception as error:
    # handling general errors
    # should be placed after all specified errors above
    print(error)

else:
    # runs when the try block is successful
    print("Division successful:", z)

finally:
    # runs regardless
    print("This code will always run.")
