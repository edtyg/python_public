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


### Mapping and Applying Functions ###

# first create your function #

def square(x):
    return(x*x)
    

## creates a new column by appyling function to an existing column ##
df1['wage_squared'] = df1['wage'].apply(square)


# you can apply function to a subset of df - just loc and filter first
# do not filter and apply function to create an existing column - will have issues
# if needed, create a temp column then replace
# key here is not to apply on filtered col, ie. wage <= 5

df1['wage_squared'] = df1.loc[df1['wage'] <= 5, 'wage'].apply(square)