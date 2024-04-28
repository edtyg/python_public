"""
using statements in loops
"""

# break is used to exit current loop prematurely
# if statement is encountered - loop is terminated
for i in range(10):
    if i == 5:
        break
    print(i)


# continue is to skip rest of loop - and moves to next iterations
for i in range(10):
    if i == 5:
        continue
    print(i)


# pass statement is used as a place holder that does nothing
for i in range(10):
    pass
