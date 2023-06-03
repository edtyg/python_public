# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 12:50:25 2023

@author: Administrator
"""

import os
import patoolib

filepath = 'C:/Users/Administrator/OneDrive/Desktop/2022 CME DATA/'
months = os.listdir(filepath)

for month in months:
    month_filepath = filepath + month
    days = os.listdir(month_filepath)
    for day in days:
        day_filepath = month_filepath + '/' + day + '/EOD' + '/XCME'
        # print(day_filepath)
        files = os.listdir(day_filepath)
        for file in files:
            rar_directory = day_filepath + '/' + file
            patoolib.extract_archive(rar_directory, outdir = day_filepath)
            print(rar_directory)