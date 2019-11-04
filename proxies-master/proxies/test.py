import asyncio


async def parse(i):
    try:
        print('*'*50, i)
    except:
        print(111111111111111111)


async def start():
    tacks = [asyncio.create_task(parse(i)) for i in range(100)]
    await asyncio.gather(*tacks)


asyncio.run(start())