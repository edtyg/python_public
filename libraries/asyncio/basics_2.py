import asyncio


async def testing():
    print("1")
    await asyncio.sleep(3)
    print("2")


async def main():
    task = asyncio.create_task(
        testing()
    )  # once we have some idle time work on this task

    await asyncio.sleep(1)  # force wait
    print("B")
    await task


if __name__ == "__main__":
    asyncio.run(main())
