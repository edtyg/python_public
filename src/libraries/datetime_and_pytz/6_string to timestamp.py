import datetime as dt

timestring = "18/09/19 01:55:19"
out = dt.datetime.strptime(timestring, "%d/%m/%y %H:%M:%S").timestamp()
print(out)
print(type(out))

# string -> datetime -> timestamp
