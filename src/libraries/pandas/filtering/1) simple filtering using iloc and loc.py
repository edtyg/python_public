import pandas as pd

data_dict = {'wage': [3.10, 3.24, 3.00, 6.00, 5.30, 8.75],
             'educ': [11.0, 12.0, 11.0, 8.0, 12.0, 16.0],
             'exper': [2.0, 22.0, 2.0, 44.0, 7.0, 9.0],
             'gender': ['Female', 'Female', 'Male', 'Male', 'Male', 'Male'],
             'married': [False, True, False, True, True, True]}

df_new = pd.DataFrame(data_dict, index = ['Mary', 'Ann', 'John', 'David', 'Frank', 'Ben'])    # Create a DataFrame object
print(df_new)

### iloc - integer based selection ###
# selection starts from 0

df_new.iloc[0] # 1st row
df_new.iloc[:,0] # 1st column

df_new.iloc[1:3, 2:3] # (2nd to 3rd row - 4th row excluded) and (3rd to 4th column - 4th column excluded)

df_new.iloc[[1,4], [2,4]] # (2nd and 5th row)  and (2nd and 5th col)


### loc - label based selection ###
# df_new's index are all names, otherwise 0,1... would suffice

df_new.loc['Mary', 'gender'] # index = mary, column = gender
df_new.loc['Mary':, 'gender'] # index = from mary onwards, column = gender

df_new.loc['Mary'] # index = Mary
