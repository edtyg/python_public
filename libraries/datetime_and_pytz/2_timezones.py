import datetime as dt
import pytz

tz = pytz.all_timezones  # list of timezones
print(tz)

# create datetime instance with timezone
timezone = pytz.timezone("Asia/Singapore")  # set time zone
d1_tz = dt.datetime.now(timezone)  # create datetime with timezone
print(d1_tz)

# add timezone to existing datetime instance
d1 = dt.datetime.now()
timezone = pytz.timezone("UTC")  # set time zone
d1 = timezone.localize(d1)  # add timezone to datetime
print(d1)

# remove timezone
d1_remove_tz = d1.replace(tzinfo=None)
print(d1_remove_tz)
