import datetime as dt

# strftime = formatting time

date = (
    dt.datetime.now()
)  # year, month, day, hour, minute, second, microsecond # creating a datetime
date_string = str(date)
print(date)

d1 = date.strftime(
    "%Y/%m/%d %H:%M:%S"
)  # outputs datetime into string  mm/dd/yyyy, hh:mm:ss
print(d1)

d1_ms = date.strftime(
    "%Y/%m/%d %H:%M:%S.%f"
)  # outputs datetime into string  mm/dd/yyyy, hh:mm:ss.ms
print(d1_ms)

d2 = date.strftime("%d %b, %Y")  # dd mmm, yyyy
print(d2)

d3 = date.strftime("%d %B, %Y")  # dd month, yyyy
print(d3)

d4 = date.strftime("%I%p")  #
print(d4)
