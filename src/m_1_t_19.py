import unittest.mock
from collections import OrderedDict
from functools import wraps


def lru_cache(*args, **kwargs):
    CACHE = OrderedDict()

    def decorator(func):
        @wraps(func)
        def wrapper(*f_args, **f_kwargs):
            function_name = str(func).split(" ")[
                1
            ]  # func.__name__ doesn't work because of unittest.mock
            key = function_name + str(f_args) + str(sorted(f_kwargs))
            if key in CACHE:
                CACHE.move_to_end(key)
                return CACHE[key]
            if maxsize := kwargs.get("maxsize"):
                if len(CACHE) > maxsize:
                    CACHE.clear()
                elif len(CACHE) == maxsize:
                    CACHE.popitem(last=False)

            res = func(*f_args, **f_kwargs)
            CACHE[key] = res

            return res

        return wrapper

    if args and callable(args[0]) and not kwargs:
        return decorator(args[0])
    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4
