from typing import TypeVar, Union

T = TypeVar("T", int, float)


Number = float | int


def add(x: Number, y: Number) -> Number:
    return x + y


def calc(a: T, b: T) -> T:
    return a + b


if __name__ == '__main__':
    print(calc(3, 4))
    print(calc([3, 4, 5], ["asdf", 12]))
