import asyncio
import json

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
    "https://httpbin.org/delay/2",
    "https://habr.com",
    "https://reddit.com",
]


async def fetch_urls(
    urls: list[str], file_path: str, concurrency: int = 5, timeout: int = 1
):
    semaphore = asyncio.Semaphore(concurrency)
    active_requests = 0  # to track restriction for simultaneous requests

    async def fetch(url: str) -> dict[str, str | int]:
        async with semaphore:
            nonlocal active_requests
            active_requests += 1
            print(f"started {url}, active requests: {active_requests} / {concurrency}")
            async with aiohttp.ClientSession() as session:
                try:
                    response = await session.get(url, timeout=timeout)
                    status = response.status
                except (asyncio.TimeoutError, aiohttp.ClientConnectorError):
                    status = 0
                active_requests -= 1
                print(
                    f"finished {url}, active requests: {active_requests} / {concurrency}"
                )
                return {"url": url, "status": status}

    coros = [fetch(url) for url in urls]
    results = await asyncio.gather(*coros)

    with open(file_path, "w") as f:
        for result in results:
            json.dump(result, f)
            f.write("\n")


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "src/m_3_t_10/results.jsonl"))
