# keywords
# coroutines, tasks, futures, await/async
# don't need to wait for something to be done to start on next task
# await = checkpoint where it is safe to go to another coroutine - will run next while waiting for current 1

import asyncio
import time

# while using spyder
import nest_asyncio
nest_asyncio.apply()

async def testing():
    # coroutine object
    start_time = time.time()
    print('hello world')
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)

async def testing_await(sleep_time: int):
    print('hello world')
    await asyncio.sleep(sleep_time)
    print('complete')


async def tasks():
    start_time = time.time()

    task1 = asyncio.create_task(testing_await(1))
    task2 = asyncio.create_task(testing_await(3))
    await task1
    await task2

    end_time = time.time()
    time_elapsed = end_time - start_time
    print(time_elapsed)


if __name__ == "__main__":
    # asyncio.run(testing())
    # asyncio.run(testing_await(1))
    # asyncio.run(tasks())
