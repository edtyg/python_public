import pandas as pd


df = pd.DataFrame({'col2': [1,2,3], 'column1': [2,3,4], 'col1':[10,20,30]}, index=[0,1,2])

df.sort_values(by=['column1'], inplace=True) # sort by column1 default = ascending

df.sort_values(by=['column1'], ascending = False, inplace=True) # sort by column1 descending

df.sort_values(by=['col1', 'col2']) # sort by multiple columns