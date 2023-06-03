# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:26:57 2022

@author: Edgar Tan
"""

def length(x):
    l = len(x)
    return(l)

# use question marks to find description

# length?
# length??

data = [1,2,3]
# data. # l.<tab> - press tab to show all attributes and methods for list type


# magic functions
%time length([1]) # single run
%timeit length([1]) # multiple run to find average
%prun length([1])
%memit length([1])

print(1)
print(_) # print last output
print(__) # print 2nd last output
