import asyncio
import json
from typing import Any

import aiofiles
import aiohttp


async def write(output_path: str, data: dict[str, str | Any]) -> None:
    async with aiofiles.open(output_path, "a") as f:
        await f.write(json.dumps(data) + "\n")


async def fetch(
    url: str,
    output_path: str,
    semaphore: asyncio.Semaphore,
    session: aiohttp.ClientSession,
    timeout: int = 1,
) -> None:
    async with semaphore:
        try:
            response = await session.get(url, timeout=timeout)
        except (asyncio.TimeoutError, aiohttp.ClientConnectorError) as e:
            print(f"Error {e} while fetching {url}")
            return
        if response.status != 200:
            print(f"Non-200 status code from {url}, status: {response.status}")
            return
        if "application/json" not in response.headers.get("Content-Type", ""):
            print(f"Non-JSON response from {url}")
            return
        try:
            response_json = await response.json()
        except aiohttp.ContentTypeError:
            print(f"Error parsing JSON from {url}")
            return

        data = {"url": url, "content": response_json}
        await write(output_path, data)


async def fetch_urls(
    input_path: str, output_path: str, concurrency: int = 5, timeout: int = 1
) -> None:
    semaphore = asyncio.Semaphore(concurrency)
    tasks = []
    async with aiohttp.ClientSession() as session:
        async with aiofiles.open(input_path, "r") as f:
            async for line in f:
                url = line.strip()
                task = asyncio.create_task(
                    fetch(url, output_path, semaphore, session, timeout)
                )
                tasks.append(task)
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(fetch_urls("src/m_3_t_21/urls.txt", "src/m_3_t_21/results.jsonl"))
