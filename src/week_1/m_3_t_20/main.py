import concurrent.futures as cf
import multiprocessing as mp
from datetime import datetime
from functools import wraps
from random import randint

import pandas as pd


def measure_time(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> float:
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        return result, (end - start).total_seconds()

    return wrapper


def generate_data(n: int) -> list[int]:
    return [randint(0, 1000) for _ in range(n)]


def process_number(number: int) -> int:
    res = 1
    for i in range(1, number + 1):
        res *= i
    return res


@measure_time
def use_sequential(data: list[int]) -> None:
    list(map(process_number, data))


@measure_time
def use_concurrent_futures(data: list[int]) -> None:
    with cf.ThreadPoolExecutor() as executor:
        list(executor.map(process_number, data))


@measure_time
def use_multiprocessing_pool(data: list[int]) -> None:
    with mp.Pool(processes=mp.cpu_count()) as pool:
        pool.map(process_number, data)


def worker(request_queue: mp.Queue, response_queue: mp.Queue) -> None:
    print("worker started")
    while True:
        task = request_queue.get()
        if task is None:
            break
        result = process_number(task)
        response_queue.put(result)


@measure_time
def use_multiprocessing_process(data: list[int]) -> None:
    response_queue = mp.Queue()
    request_queue = mp.Queue()
    cpu_count = mp.cpu_count()
    max_processes = min(cpu_count, len(data))
    processes = []

    for _ in range(max_processes):
        process = mp.Process(target=worker, args=(request_queue, response_queue))
        processes.append(process)

    for process in processes:
        process.start()

    for task in data:
        request_queue.put(task)

    for _ in range(max_processes):
        request_queue.put(None)

    results = []
    for _ in range(len(data)):
        result = response_queue.get()
        results.append(result)

    for process in processes:
        process.join()


def get_results(functions: list[callable]) -> dict[str, float]:
    data = generate_data(100000)
    results = {func.__name__: func(data)[1] for func in functions}
    return results


def store_results(file_path: str) -> None:
    results = get_results(
        [
            use_sequential,
            use_concurrent_futures,
            use_multiprocessing_pool,
            use_multiprocessing_process,
        ]
    )
    data = {
        "function": list(results.keys()),
        "time_seconds": list(results.values()),
        "performance_vs_sequential": [
            results["use_sequential"] / time for time in results.values()
        ],
    }

    df = pd.DataFrame(data)
    df.to_json(file_path, orient="records", lines=True, indent=4)


if __name__ == "__main__":
    store_results("src/week_1/m_3_t_20/results.jsonl")
