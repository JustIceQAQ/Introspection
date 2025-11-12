import asyncio
import concurrent.futures
from pprint import pprint


def task(index: int, sec: int):
    import time
    time.sleep(sec)
    return f"{index} task sleep {sec} , done"


async def main():
    executor = concurrent.futures.ProcessPoolExecutor()
    loop = asyncio.get_running_loop()
    tasks = []
    for i in range(1, 11):
        tasks.append(loop.run_in_executor(executor, task, *(i, i % 3,)))
    results = await asyncio.gather(*tasks)

    pprint(results)


if __name__ == '__main__':
    asyncio.run(main())
