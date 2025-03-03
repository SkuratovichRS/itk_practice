import asyncio
import json
from typing import Any

import aiofiles
import aiohttp


async def producer(queue: asyncio.Queue, input_path: str) -> None:
    print("producer started")
    async with aiofiles.open(input_path, "r") as f:
        async for line in f:
            url = line.strip()
            await queue.put(url)
            print(f"producer put {url}, {queue.qsize()=}")
        for _ in range(queue.qsize()):
            await queue.put(None)
            print(f"producer put None, {queue.qsize()=}")
        print("producer finished")


async def consumer(
    queue: asyncio.Queue,
    session: aiohttp.ClientSession,
    lock: asyncio.Lock,
    timeout: int,
    output_path: str,
) -> None:
    while True:
        print(f"consumer started, {queue.qsize()=}")
        url = await queue.get()
        print(f"consumer get {url} {queue.qsize()=}")
        if url is None:
            break
        data = await fetch(url, session, timeout)
        if data is None:
            continue
        async with lock:
            async with aiofiles.open(output_path, "a") as f:
                await f.write(json.dumps(data) + "\n")
    print("consumer finished")


async def fetch(
    url: str,
    session: aiohttp.ClientSession,
    timeout: int,
) -> dict[str, str | Any]:
    print(f"fetching {url}")
    try:
        response = await session.get(url, timeout=timeout)
    except (asyncio.TimeoutError, aiohttp.ClientConnectorError):
        return
    if response.status != 200:
        return
    if "application/json" not in response.headers.get("Content-Type", ""):
        return
    try:
        response_json = await response.json()
    except aiohttp.ContentTypeError:
        return

    data = {"url": url, "content": response_json}
    return data


async def fetch_urls(
    input_path: str, output_path: str, concurrency: int = 5, timeout: int = 1
) -> None:
    consumer_tasks = []
    queue = asyncio.Queue(maxsize=concurrency)
    lock = asyncio.Lock()
    producer_task = asyncio.create_task(producer(queue, input_path))

    async with aiohttp.ClientSession() as session:
        for _ in range(concurrency):
            consumer_task = asyncio.create_task(
                consumer(queue, session, lock, timeout, output_path)
            )
            consumer_tasks.append(consumer_task)

        await asyncio.gather(producer_task, *consumer_tasks)


if __name__ == "__main__":
    asyncio.run(fetch_urls("src/m_3_t_21/urls.txt", "src/m_3_t_21/results.jsonl"))
