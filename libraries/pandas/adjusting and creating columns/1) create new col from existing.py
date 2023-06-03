import pandas as pd
import numpy as np

data_dict = {'wage': [3.10, 3.24, 3.00, 6.00, 5.30, 8.75, np.nan, np.nan],
             'education': [11.0, 12.0, 11.0, 8.0, 12.0, 16.0, np.nan, np.nan],
             'experience': [2.0, 22.0, 2.0, 44.0, 7.0, 9.0, np.nan, np.nan],
             'gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male', np.nan, np.nan],
             'married': [False, True, False, True, True, True, np.nan, True],
             'symbol': ['BTC-USD', 'BTC-USDT', 'ETH-USD', 'ETH-USDT', 'USDT-USD', 'BNB-BUSD', 'CAKE-BUSD', 'DOGE-USD'],
             'symbol2': ['BTC-USD_01', 'BTC-USD_02', 'ETH-USD_01', 'ETH-USDT_01', 'USDT-USD_02', 'BNB-BUSD_05', 'CAKE-BUSD_08', 'DOGE-USD']
             }

df1 = pd.DataFrame(data_dict)    # Create a DataFrame object
print(df1)

### simple column creation ###
df1['new_column'] = 'testing' # creates new column with name = 'new_column, with all the values = 'testing'

# loops through columnn = 'education'
# if value > 12 new value = 1 else value = 0
# new values created in new column = 'highly_educated'
df1['highly_educated'] = [1 if x > 12 else 0 for x in df1['education']]

## similar to above, but with more customisation ##
df1.loc[df1['existing column'] > 1 ,'new col'] = 1 # if current col has values > 1, creates New column with value 1
df1.loc[df1['existing column'] <= 1 ,'new col'] = 2 # if current col has values <= 1, creates New column with value 2

## similar to above but with starts with string ##
df1.loc[df1['Current Column'].str.startswith('BTC') , 'New Col Name'] = 'BTC' # current col has values that starts with BTC -> creates new col with value 'BTC'
df1.loc[df1['Current Column'].str.startswith('ETH') , 'New Col Name'] = 'ETH' # current col has values that starts with BTC -> creates new col with value 'ETH'

## aggregate of 2 other columns ##
df1['new col name'] = df1['current col 1'] + df1['current col 2'] # summing up 2 columns and creating a new col
df1['wage_after_tax'] = df1['wage'] * 0.8


# do a loop through index same outcome as above
for i in df1.index:
    if df1.loc[i, 'education'] > 12:
        df1.loc[i, 'highly_educated'] = 1
    else:
        df1.loc[i, 'highly_educated'] = 0