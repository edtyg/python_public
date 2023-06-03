# lists are mutable
# mutable version of tuples

l = []
type(l)

l = ["sword", "shield", "bow", "bow"]

l.sort()  # this changes the list

l.append("spear")  # can only append one element

l.reverse()

l.count("bow")

l.index("bow")  # position of first bow

l.insert(1, "arrow")  # adds arrow to position 1

l.remove("bow")  # removes first instance of bow

l.pop()  # removes last item

l.pop(1)  # removes i th item in list
