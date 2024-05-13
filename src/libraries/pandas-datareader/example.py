"""
pip install pandas-datareader
pulls prices
"""

import pandas_datareader as pdr

data = pdr.get_data_fred("GS10")
print(data)
