import datetime as dt
import pytz

# listing all timezones
pytz.all_timezones

# creating a datetime instance with timezone
d1_custom = dt.datetime(2022, 1, 1, 0, 0, 0, 100, tzinfo=pytz.utc)
# year, month, day, hour, minute, second, microsecond, timezone info

# specify timezone
timezone = pytz.timezone("Singapore")
d2_custom = dt.datetime(2022, 1, 1, 1, 1, 1, 1, tzinfo=timezone)

print("now")
d1 = dt.datetime.now(timezone)  # singapore timezone
print(d1)

print("current date")
print(d1.date())  # returns year, month, day

print("current time")
print(d1.time())  # returns hour, minute, second

print("year")
print(d1.year)

print("month")
print(d1.month)

print("day")
print(d1.day)

print("hour")
print(d1.hour)

print("minute")
print(d1.minute)

print("second")
print(d1.second)

print("microsecond")
print(d1.microsecond)

print("day of week")
print(d1.isoweekday())

dt.datetime.now()  # returns current date and time
dt.datetime.today()  # returns current date and time
