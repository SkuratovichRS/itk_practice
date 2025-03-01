import concurrent.futures as cf
import multiprocessing as mp
from datetime import datetime
from functools import wraps
from random import randint

import pandas as pd


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        end = datetime.now()
        return (end - start).total_seconds()

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


def task(task_data: list[int], queue: mp.Queue) -> None:
    queue.put([process_number(i) for i in task_data])
    queue.put(None)


@measure_time
def use_multiprocessing_process(data: list[int]) -> None:
    queue = mp.Queue()
    cpu_count = mp.cpu_count()
    max_processes = min(cpu_count, len(data))
    chunk_size = len(data) // max_processes
    processes = []

    for i in range(max_processes):
        start = i * chunk_size
        end = start + chunk_size if i < max_processes - 1 else len(data)
        process = mp.Process(target=task, args=(data[start:end], queue))
        process.start()
        processes.append(process)

    finished_processes = 0
    result = []
    while (
        finished_processes < max_processes
    ):  # without manual check, main process is blocked at the join stage
        item = queue.get()
        if item is None:
            finished_processes += 1
        else:
            result.extend(item)

    for process in processes:
        process.join()


def get_results(functions: list[callable]) -> None:
    data = generate_data(100000)
    results = {func.__name__: func(data) for func in functions}
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
    store_results("src/m_3_t_20/results.jsonl")
