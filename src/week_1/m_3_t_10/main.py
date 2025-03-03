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

    async def fetch(url: str) -> dict[str, str | int]:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                try:
                    response = await session.get(url, timeout=timeout)
                    status = response.status
                except (asyncio.TimeoutError, aiohttp.ClientConnectorError):
                    status = 0
                return {"url": url, "status": status}

    coros = [fetch(url) for url in urls]
    results = await asyncio.gather(*coros)

    with open(file_path, "w") as f:
        for result in results:
            json.dump(result, f)
            f.write("\n")


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "src/m_3_t_10/results.jsonl"))
