from functools import wraps


def async_retry(retries: int, exceptions: tuple = (Exception,)) -> callable:
    def decorator(func) -> callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    print(f"Retrying unstable_task ({i + 1}/{retries})...")
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if i == retries - 1:
                        raise e

        return wrapper

    return decorator
