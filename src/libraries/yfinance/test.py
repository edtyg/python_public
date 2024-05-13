"""
pip install yfinance
pip install pandas
https://pypi.org/project/yfinance/
"""

import yfinance as yf
import pandas as pd

msft = yf.Ticker("MSFT")

data = msft.history(period="1d", start="2023-01-01", end="2023-12-31")
data = data[["Close"]]
