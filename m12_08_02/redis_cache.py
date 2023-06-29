import timeit

import redis
from redis_lru import RedisLRU

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def fib(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


@cache
def fib_cache(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_cache(n - 1) + fib_cache(n - 2)


@cache
def baz(l_num: list) -> int:
    print(f"Inner: {l_num}")
    return sum(l_num)


@cache
def foo(a, b) -> int:
    print(f"Inner foo: {a} {b}")
    return a + b


if __name__ == '__main__':
    # start = timeit.default_timer()
    # r = fib(35)
    # print(f"Result fib(25): {timeit.default_timer() - start}: {r}")
    #
    # start = timeit.default_timer()
    # r = fib_cache(35)
    # print(f"Result fib_cache(25): {timeit.default_timer() - start}: {r}")

    nums = (1, 2, 3, 4)
    r = baz(nums)
    print(r)
    r = baz(nums)
    print(r)

    r = foo("str", "abc")
    print(r)
    r = foo("str", "abc")
    print(r)
