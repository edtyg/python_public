# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 14:22:06 2021

@author: Edgar Tan
"""
# https://numpy.org/doc/stable/user/basics.creation.html

import numpy as np

# creates an array from a python list
array_1d = np.array([1,2,3])

# 6x3 array
array_2d = np.array(
    [
     [18, 26, 17], 
     [25, 15.5, 12], 
     [24, 27, 20],
     [10, 5.5, 17],
     [27, 26, 15],
     [22, 21, 21],
     ]
    ) 


print(array_2d.ndim) # dimensions
print(array_2d.shape)
print(array_2d.size)
print(array_2d.dtype)

# 3d arrays
zero = np.zeros(shape=(3,3,3))
print(zero)

ones = np.ones(shape=(3,3,3))
print(ones)

# fill with value of your choice
fill = np.full(shape = (3,3), fill_value = 3.14)
print(fill)

array_2d[0] #1st row
array_2d[:,0] #1st col

array_2d[0][0] #1st element - 1st row 1st col
array_2d[2:] #3rd row onwards
array_2d[:2] #1st and 2nd row

test1 = array_2d[:,2:]
test2 =  array_2d[:,2]
