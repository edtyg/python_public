# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 14:19:46 2022

@author: Edgar Tan
"""

# https://www.youtube.com/watch?v=fKl2JW_qrso&t=1s

import time
import multiprocessing
import logging
import os

# logging #
full_path = os.path.realpath(__file__) # C:\Users\Edgar Tan\OneDrive\Github\python\os\1) Basics.py
save_path = os.path.dirname(full_path) + "/"
log_file = 'logging_example.log'

logging.basicConfig(
    filename = save_path + log_file,
    level = logging.DEBUG, # set default to DEBUG
    format ='%(asctime)s:%(levelname)s:%(message)s',
    filemode ='a' # 'w' = write = create new file each time, 'a' = append = append each log
) 

logger = logging.getLogger(__name__)
###

def do_something(time_second: int):
    logging.info('sleeping')
    print(f'sleeping for {time_second} seconds')
    time.sleep(time_second)
    print('done sleeping')
    

if __name__ == "__main__":
    
    start = time.perf_counter()
    
    processes = []
    
    for _ in range(200):
        p = multiprocessing.Process(target = do_something, args = [1])
        p.start()
        processes.append(p)
    
    for process in processes:
        process.join()
    
    finish = time.perf_counter()
    elasped_time = finish - start
    
    print(f'total elasped time = {elasped_time}')
