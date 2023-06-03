import datetime as dt

# strptime = parse time

# %d - day of the month (01 to 31)
# %m - month (01 to 12)
# %y - year without a century  - 21
# %Y - year including the century - 2021


# %H - hour, using a 24-hour clock (00 to 23)
# %I - hour, using a 12-hour clock (01 to 12)

# %M - minute - small m = month
# %S - second

# %p - either am or pm according to the given time value

# %r - time in a.m. and p.m. notation


# https://www.tutorialspoint.com/python/time_strptime.htm

timestring_1 = "18/09/2019 12:55:19"
out = dt.datetime.strptime(timestring_1, "%d/%m/%Y %H:%M:%S")
print(out)
print(type(out))

timestring_2 = "2022-03-01 12:20:10+00:00"
out = dt.datetime.strptime(timestring_2, "%Y-%m-%d %H:%M:%S%z")
print(out)
print(type(out))

# with milliseconds and timezone
timestring_3 = "2022-09-09T02:00:39.357220+00:00"
out = dt.datetime.strptime(timestring_3, "%Y-%m-%dT%H:%M:%S.%f%z")
print(out)
print(type(out))
