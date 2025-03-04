import random
import time

import redis


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, client: redis.Redis, queue_name: str = "queue"):
        self._client = client
        self._queue_name = queue_name

    def test(self) -> bool:
        current_time = time.time()

        while self._client.llen(self._queue_name) > 0:
            last_request_time = float(self._client.lindex(self._queue_name, -1))
            if current_time - last_request_time > 3:
                self._client.rpop(self._queue_name)
            else:
                break

        if self._client.llen(self._queue_name) >= 5:
            return False
        else:
            self._client.lpush(self._queue_name, current_time)
            return True


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        pass


if __name__ == "__main__":
    rate_limiter = RateLimiter(redis.Redis("localhost", port=6379))

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
