# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:34:17 2022

@author: Edgar Tan
"""
import pandas as pd

d = {
     'id': [1,1,2,2,3,3,3,4,4,4],
     'value1': [1,2,3,4,5,6,7,8,9,10],
     }

df = pd.DataFrame(d)


empty_df = pd.DataFrame()
for i in df.columns.tolist():
    # loops through your columns
    series = df[i] # reads your column and creates a series dimensions = 1 x n
    counts = series.value_counts() # count unique objects
    counts_df = pd.DataFrame(df[i].value_counts()) # creates df 
    counts_df.rename(columns = {i:'value'}, inplace=True) # renames the header name to value
    counts_df['column_name'] = i # stores col names
    empty_df = pd.concat([empty_df, counts_df])
empty_df.reset_index(drop=True, inplace=True)
print(empty_df)