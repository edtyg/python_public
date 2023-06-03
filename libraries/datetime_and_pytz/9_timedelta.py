import datetime as dt

d1 = dt.datetime(
    2021, 1, 14, 10, 15, 0, 0
)  # year, month, day, hour, minute, second, microsecond # creating a datetime
delta = dt.timedelta(hours=1)

d2 = d1 - delta

# time delta methods
delta.days
delta.seconds
