# example of using an event object with processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Event

import os
import logging

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
 
# target task function
def task(event, number):
    # wait for the event to be set
    print(f'Process {number} waiting...', flush=True)
    event.wait()
    # begin processing
    value = random()
    sleep(value)
    print(f'Process {number} got {value}', flush=True)
 
# entry point
if __name__ == '__main__':
    # create a shared event object
    event = Event()
    
    # create a suite of processes
    processes = [Process(target=task, args=(event, i)) for i in range(5)]
    
    # start all processes
    for process in processes:
        process.start()
        
    # block for a moment
    print('Main process blocking...')
    sleep(2)
    # trigger all child processes
    
    event.set()
    # wait for all child processes to terminate
    for process in processes:
        process.join()