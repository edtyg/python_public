import datetime as dt


ts = 1648867374.5  # only 10 digits + decimal

out = dt.datetime.fromtimestamp(ts)  # convert timestamp to datetime object

print(out)
print(type(out))


# https://www.epochconverter.com/
# convert timestamp to datetime
