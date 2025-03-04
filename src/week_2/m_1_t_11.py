import json

import redis


class RedisQueue:
    def __init__(self, client: redis.Redis, queue_name: str = "queue"):
        self._client = client
        self._queue_name = queue_name

    def publish(self, msg: dict):
        self._client.rpush(self._queue_name, json.dumps(msg))

    def consume(self) -> dict:
        msg = self._client.lpop(self._queue_name)
        if msg is None:
            return
        return json.loads(msg)


if __name__ == "__main__":
    q = RedisQueue(redis.Redis("localhost", port=6379))
    q.publish({"a": 1})
    q.publish({"b": 2})
    q.publish({"c": 3})

    assert q.consume() == {"a": 1}
    assert q.consume() == {"b": 2}
    assert q.consume() == {"c": 3}
