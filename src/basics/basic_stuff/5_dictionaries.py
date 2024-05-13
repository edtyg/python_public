"""
Dictionaries
dict contains pairs/items
keys : value
keys have to be unique
"""

d = {"404": "clue", "123": "numb"}
type(d)

d["404"]

d.get("404")  # returns value for specified key

d.keys()
list(d.keys())

d.values()
list(d.values())

d.items()
list(d.items())

d["value"] = 1  # creating a new key/item or replacing an existing one


### writing loops for dictionaries ###
# using items more efficient

for key, value in d.items():
    print(key, value)
