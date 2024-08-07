"""
coroutines, tasks, futures, await/async
don't need to wait for something to be done to start on next task
await = checkpoint where it is safe to go to another coroutine
will run next while waiting for current checkpoint to finish

best used for i/o tasks (input/output) where theres a waiting time
api calls, database queries, reading files
"""

import asyncio
import time


async def testing():
    """
    coroutine object
    """
    start_time = time.time()
    print("hello world")
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)


async def testing_await(sleep_time: int):
    """testing asyncio.sleep"""
    print("hello world")
    await asyncio.sleep(sleep_time)
    print("complete")


async def set_tasks():
    """setting tasks
    create a list of tasks then use gather
    can use a loop to set up tasks in a list
    """
    start_time = time.time()

    task1 = asyncio.create_task(testing_await(1))
    task2 = asyncio.create_task(testing_await(3))
    tasks = [task1, task2]
    await asyncio.gather(*tasks)

    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)


if __name__ == "__main__":
    # asyncio.run(testing())
    # asyncio.run(testing_await(1))
    asyncio.run(set_tasks())
