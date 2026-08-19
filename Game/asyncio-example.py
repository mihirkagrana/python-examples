import asyncio

def one():
    print("One")

async def two():
    print("Two")
    await asyncio.sleep(3)
    print("Two finished")

async def three():
    print("Three")
    await asyncio.sleep(1)
    print("Three finished")

def four():
    print("four")

async def main():
    one()
    task1 = asyncio.create_task(two())
    task2 = asyncio.create_task(three())
    four()

    await task1
    await task2

asyncio.run(main())