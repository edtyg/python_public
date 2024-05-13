import datetime as dt


ts = 1648867374.5  # only 10 digits + decimal
out = dt.datetime.fromtimestamp(ts).strftime(
    "%Y-%m-%d %H:%M:%S"
)  # convert epoch time to string

print(out)
print(type(out))


# timestamp -> datetime -> string.
