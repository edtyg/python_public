import pandas as pd
import numpy as np


data_dict = {'wage': [3.10, 3.24, 3.00, 6.00, 5.30, 8.75, np.nan, np.nan],
             'education': [11.0, 12.0, 11.0, 8.0, 12.0, 16.0, np.nan, np.nan],
             'experience': [2.0, 22.0, 2.0, 44.0, 7.0, 9.0, np.nan, np.nan],
             'gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', np.nan, np.nan],
             'married': [False, True, False, True, True, True, np.nan, True],
             'symbol': ['BTC-USD', 'BTC-USDT', 'ETH-USD', 'ETH-USDT', 'USDT-USD', 'BNB-BUSD', 'CAKE-BUSD', 'DOGE-USD']}

df1 = pd.DataFrame(data_dict)    # Create a DataFrame object
print(df1)

df1 = df1.replace(np.NaN, 0)