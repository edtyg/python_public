import datetime as dt

date = (
    dt.datetime.now()
)  # year, month, day, hour, minute, second, microsecond # creating a datetime

out = date.timestamp()
print(out)
