import pandas as pd
import numpy as np


data_dict = {'wage': [3.10, 3.10, 3.20, 6.00, 5.30, 8.75, np.nan, np.nan],
             'education': [11.0, 11.0, 11.0, 11.0, 12.0, 16.0, np.nan, np.nan],
             'experience': [12.0, 12.0, 2.0, 44.0, 7.0, 9.0, np.nan, np.nan],
             'gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', np.nan, np.nan],
             'married': [False, False, False, True, True, True, np.nan, True],
             'symbol': ['BTC-USD', 'BTC-USD', 'ETH-USD', 'ETH-USDT', 'USDT-USD', 'BNB-BUSD', 'CAKE-BUSD', 'DOGE-USD']}

df1 = pd.DataFrame(data_dict)    # Create a DataFrame object
print(df1)

df1.drop_duplicates() # By default, it removes duplicate rows based on all columns.

df1.drop_duplicates(subset=['wage']) # drop duplicates based on column1 # will take first value
