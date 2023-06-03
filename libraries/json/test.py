# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 22:21:43 2022

@author: Administrator
"""

import json


d = {'a': 1, 'b': 2}

data_string = json.dumps(d) # dictionary to string
print(data_string)

data_dict = json.loads(data_string) # string to dictionary
print(data_dict)
