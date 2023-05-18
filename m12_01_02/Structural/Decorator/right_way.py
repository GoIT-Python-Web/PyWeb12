import time
from functools import wraps


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(* args, ** kwargs)
        end = time.time()
        print(f"{func.__name__}: Time: {end - start}")
        return result
    return wrapper


@logger
def my_func(num: int):
    """
    My function
    :param num:
    :return:
    """

    while num > 0:
        num -= 1


if __name__ == '__main__':
    my_func(1_000_000)

    print(f"Function name: {my_func.__name__}")
    print(f"Function docstring: {my_func.__doc__}")
    print(f"Function annotation: {my_func.__annotations__}")

    my_func.__wrapped__(1_000_000)  # noqa
