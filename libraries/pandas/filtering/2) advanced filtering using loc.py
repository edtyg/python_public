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

### examples here ###

#### filter rows by only 1 condition ###
df1.loc[df1['wage'] >= 5] # filter rows where wage >= 5

df1.loc[df1['wage'].isin([3,6])] # filter rows where symbol in list 

df1.loc[df1['symbol'].str.startswith('BTC')] # filter rows where symbol starts with BTC
df1.loc[~df1['symbol'].str.startswith('BTC')] # filter rows where symbol does not start with BTC - add ~ in front

df1.loc[df1['married'] == True] # filters bool

df1.loc[df1['symbol'].str.contains('BTC-USD', 'BTC-USDT')] # filter rows where symbol in list


### filter rows by only 1 condition and select columns ###
df1.loc[df1['wage'] <= 5, ['wage','education']] # filter rows where wage >= 5 and showing cols wage and education
df1.loc[df1['wage'] <= 5, ['education','experience']] # filter rows where wage >= 5 and showing cols education and experience



### filter by 2 or more conditions ###
# note: usage of brackets important here #
# bracket each condition, then bracket the whole thing, added in some spaces to see clearer

# using 'and' conditional - note that you need to use & for df filters instead of 'and'
df1.loc[  ((df1['symbol'] == 'BTC-USD') & (df1['gender'] == 'Female'))  ]

# using 'or' conditional - note that you need to use | for df filters instead of 'or
df1.loc[  ((df1['symbol'] == 'BTC-USD') | (df1['gender'] == 'Female'))  ]

### filter rows by only 2 or more conditions and select columns ###
df1.loc[((df1['symbol'] == 'BTC-USD') & (df1['gender'] == 'Female')), ['wage', 'education']]