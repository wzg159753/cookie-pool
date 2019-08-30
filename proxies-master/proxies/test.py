import asyncio


def func(i):
    print(f'我是{i}')


track = [func(i) for i in range(20)]
asyncio.gather(*track)