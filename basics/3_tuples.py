# tuples are immutable
# cannot change once they are created
# have to create a new tuple if any

t = ()
type(t)

t = ("sword", "shield", "sword")
print(t)

for i in t:
    print(i)

len(t)

t[0]
t[1]
t[-1]


t.count("")  # count number of times value occurs in the tuple
t.index("sword")  # find the index of the first instance of sword

t + t
