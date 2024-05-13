# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 10:10:40 2021

@author: Edgar Tan
"""

import pandas as pd

###################################################
### creating a pandas dataframe from dictionary ###

dataset1 = {'a':[4,5,6],
           'b':[7,8,9],
           'c':[10,11,12]
           }
index1 = [1,2,3]

df1 = pd.DataFrame(dataset1, index = index1)
print(df1)

df1.rename(columns = {'a':'new'}, inplace=True)