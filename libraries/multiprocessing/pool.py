# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 13:31:34 2022

@author: Edgar Tan
"""

import multiprocessing
import os
import time


def task_sleep(sleep_duration, task_number):
    time.sleep(sleep_duration)
    print(f"Task {task_number} done (slept for {sleep_duration}s)! "
          f"Process ID: {os.getpid()}")


if __name__ == "__main__":
    time_start = time.time()

    # Create pool of workers
    pool = multiprocessing.Pool(2)

    # Map pool of workers to process
    pool.starmap(func=task_sleep, iterable=[(2, 1), (3,2)])

    # Wait until workers complete execution
    pool.close()

    time_end = time.time()
    print(f"Time elapsed: {round(time_end - time_start, 2)}s")

    # Task 1 done (slept for 2s)! Process ID: 20464
    # Task 1 done (slept for 2s)! Process ID: 22308
    # Task 1 done (slept for 2s)! Process ID: 20464
    # Task 1 done (slept for 2s)! Process ID: 22308
    # Task 1 done (slept for 2s)! Process ID: 20464
    # Task 1 done (slept for 2s)! Process ID: 22308
    # Task 1 done (slept for 2s)! Process ID: 20464
    # Task 1 done (slept for 2s)! Process ID: 22308
    # Task 1 done (slept for 2s)! Process ID: 20464
    # Task 1 done (slept for 2s)! Process ID: 20464
    # Time elapsed: 12.58s