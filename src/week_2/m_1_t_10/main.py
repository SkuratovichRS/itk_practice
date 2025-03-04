import datetime
import threading as th
import time
from functools import wraps
from unittest import TestCase

from redlock import Redlock

print_lock = th.Lock()
dlm = Redlock([{"host": "127.0.0.1", "port": 6379}])


def single(max_processing_time: datetime.timedelta) -> callable:
    def decorator(func) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            max_processing_time_ms = int(max_processing_time.total_seconds() * 1000)
            lock_name = func.__name__
            lock_instance = dlm.lock(lock_name, max_processing_time_ms)
            if not lock_instance:
                with print_lock:
                    print(
                        f"Could not acquire lock for {lock_name}, {th.current_thread().name} "
                    )
                return

            try:
                return func(*args, **kwargs)
            finally:
                dlm.unlock(lock_instance)

        return wrapper

    return decorator


def run_threads(
    run_task_sec: int, max_threads: int = 10, sleep_time: int = 0
) -> list[int]:
    test_concurrency = []
    threads = []
    for _ in range(max_threads):
        thread = th.Thread(target=some_function, args=(run_task_sec, test_concurrency))
        time.sleep(sleep_time)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return test_concurrency


@single(datetime.timedelta(seconds=0.3))
def some_function(run_time_sec: int, test_concurrency) -> None:
    with print_lock:
        print(f"Starting task, {th.current_thread().name}")
        test_concurrency.append(1)
    time.sleep(run_time_sec)
    with print_lock:
        print(f"finished task, {th.current_thread().name}")
        test_concurrency.append(0)


def test_dumb(result: list[int]) -> None:
    for i in range(len(result)):
        if i % 2 == 0:
            assert result[i] == 1
        else:
            assert result[i] == 0


if __name__ == "__main__":
    test_dumb(run_threads(run_task_sec=0.2, sleep_time=0.05))
    with TestCase().assertRaises(AssertionError):
        test_dumb(run_threads(run_task_sec=0.6, sleep_time=0.2))
