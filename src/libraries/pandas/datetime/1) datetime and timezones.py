"""
testing
"""
import datetime as dt
import pandas as pd
import pytz

timezone = pytz.timezone("UTC")  # set time zone

# string and int format #
time = {
    "timestring": ["2020-01-01T07:00:00", "2021-01-01T07:00:00"],  # string
    "timestring_with_decimals": [
        "2020-01-01T07:00:00.10",
        "2021-01-01T07:00:00.10",
    ],  # string
    "timestring_with_decimals_tz": [
        "2020-01-01T07:00:00.10+08",
        "2021-01-01T07:00:00.10+08",
    ],  # string
    "timestamp": [1577862000000, 1609484400000],  # int
    "datetime": [
        dt.datetime(2020, 1, 1, 7, 0, 0),
        dt.datetime(2021, 1, 1, 7, 0, 0),
    ],  # datetime
    "datetime_with_tz": [
        timezone.localize(dt.datetime(2020, 1, 1, 7, 0, 0)),
        timezone.localize(dt.datetime(2021, 1, 1, 7, 0, 0)),
    ],  # datetime with utc timezone
}

# sample data , date and timestamps date in string format
df = pd.DataFrame(time)
print(df)
df.dtypes

# timestring to datetime
df["datetime_from_timestring"] = pd.to_datetime(
    df["timestring"], format="%Y-%m-%dT%H:%M:%S"
)

# timestring_with_decimals to datetime
df["datetime_from_timestring_with_decimals"] = pd.to_datetime(
    df["timestring_with_decimals"], format="%Y-%m-%dT%H:%M:%S.%f"
)

# timestring_with_decimals_tz to datetime
df["datetime_from_timestring_with_decimals_tz"] = pd.to_datetime(
    df["timestring_with_decimals_tz"], format="%Y-%m-%dT%H:%M:%S.%f+08"
)

# timestamp to datetime
df["datetime_from_timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# datetime to timestring
df["timestring_from_datetime"] = df["datetime"].dt.strftime("%Y-%m-%dT%H:%M:%S")
df["timestring_from_datetime2"] = df["datetime"].dt.strftime("%d/%m/%Y %H:%M:%S")

# datetime_with_tz to datetime
df["datetime_with_tz_removed"] = df[("datetime_with_tz")].dt.tz_localize(
    None
)  # remove timezone - cannot export to excel file with tz
print(df)

# datetime to datetime_with_tz
df["datetime_with_tz_from_datetime"] = df["datetime"].dt.tz_localize("UTC")


## creates individual cols - require datetime format ##
df["year"] = pd.DatetimeIndex(df["datetime"]).year
df["month"] = pd.DatetimeIndex(df["datetime"]).month
df["day"] = pd.DatetimeIndex(df["datetime"]).day
df["hour"] = pd.DatetimeIndex(df["datetime"]).hour

## creates datetime col from individual components
df["date_from_components"] = pd.to_datetime(
    df[["year", "month", "day", "hour"]]
)  # creates a new column using year, month, day and hour columns
