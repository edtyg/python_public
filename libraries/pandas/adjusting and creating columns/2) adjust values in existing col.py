import pandas as pd
import numpy as np

data_dict = {
    'wage': [3.10, 3.24, 3.00, 6.00, 5.30, 8.75, np.nan, np.nan],
    'education': [11.0, 12.0, 11.0, 8.0, 12.0, 16.0, np.nan, np.nan],
    'experience': [2.0, 22.0, 2.0, 44.0, 7.0, 9.0, np.nan, np.nan],
    'gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', np.nan, np.nan],
    'married': [False, True, False, True, True, True, np.nan, True],
    'symbol': ['BTC-USD', 'BTC-USDT', 'ETH-USD', 'ETH-USDT', 'USDT-USD', 'BNB-BUSD', 'CAKE-BUSD', 'DOGE-USD'],
    'symbol2': ['BTC-1231', 'ETH-1231', 'BTC-0325', 'ETH-0325', 'BTC-0625', 'ETH-0625', 'BTC-0924', 'ETH-0924'],
    'type2':['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none']
             }

df1 = pd.DataFrame(data_dict)    # Create a DataFrame object
print(df1)

### change values in same column ###

df1.loc[df1['wage'] <= 5] = 10 # filter wages <= 5 and change the values of all columns to 10

df1.loc[df1['wage'] <= 5, 'wage'] = 10 # filter wages <= 5 and change the values of column = 'wage' to 10


# change values in different column - note if 'type2' is not an existing column, it will be created
df1.loc[df1['symbol2'].str.contains('1231'), 'type2'] = 'futures' # filter wages <= 5 and change the values of column = 'wage' to 10


### alternatively, u can loop through the entire df ###
### but u have to make sure index is unique ###

for i in df1.index:
    print(df1.loc[i])
    if df1.loc[i, 'wage'] <= 5:
        # creates new column poor = 1 - if col already exists, then value is adjusted
        df1.loc[i, 'poor'] = 1