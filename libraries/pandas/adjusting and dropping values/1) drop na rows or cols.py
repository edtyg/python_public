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

## drop na ##
df1.dropna(axis = 'rows', thresh = 2) # threshold = 2 means if a row has 2 or more non-na values, it will not be dropped

## drop rows or columns ##
df1.drop(['wage', 'education'], axis=1) # axis=1 means columns. Drop columns named 'wage' and 'education'
df1.drop([0,1,2], axis=0) # drop rows by their indexes

## replace na values with value of your own
df1.fillna('blank') # replace na with the string 'blank'
df1.fillna(0) # replace na with the value 0


# filter out pandas nan - different from np.nan
# pd.isnull(xxx)
