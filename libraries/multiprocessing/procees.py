# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:24:38 2022

@author: Edgar Tan
"""

# Pool method allows users to define the number of workers and distribute all processes to available processors in a First-In-First-Out schedule, 
# handling process scheduling automatically. 
# Pool method is used to break a function into multiple small parts using map or starmap(line 19) — running the same function with different input arguments. 
# Whereas Process method is used to run different functions.

import multiprocessing
import os
import time




def task_sleep(sleep_duration, task_number):
    time.sleep(sleep_duration)
    print(f"Task {task_number} done (slept for {sleep_duration}s)! "
          f"Process ID: {os.getpid()}")


if __name__ == "__main__":
    time_start = time.time()

    # Create process
    p1 = multiprocessing.Process(target=task_sleep, args=(2, 1))
    p2 = multiprocessing.Process(target=task_sleep, args=(2, 2))

    # Start task execution
    p1.start()
    p2.start()

    # Wait for process to complete execution
    p1.join()
    p2.join()

    time_end = time.time()
    print(f"Time elapsed: {round(time_end - time_start, 2)}s")

    # Task 1 done (slept for 2s)! Process ID: 11544
    # Task 2 done (slept for 2s)! Process ID: 23724
    # Time elapsed: 2.81s