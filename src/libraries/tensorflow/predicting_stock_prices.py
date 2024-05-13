"""
Predicting stock prices
"""

import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential

company = "FB"

start = dt.datetime(2024, 1, 1)
end = dt.datetime(2024, 4, 1)

data = web.DataReader(company, "yahoo", start, end)
# print(data)
