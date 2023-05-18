from enum import Enum
from abc import ABC, abstractmethod
from typing import List


class OperationType(str, Enum):
    SUM = 'sum'
    MUL = 'mul'


class Operation(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def operation(self):
        pass


class Adder(Operation):
    def __init__(self, data: List[int]):
        super().__init__()
        self.data = data

    def operation(self):
        return sum(self.data)

    @staticmethod
    def info(cls):
        return 'Adder class'


class Multiplier(Operation):
    def __init__(self, data: List[int]):
        super().__init__()
        self.data = data

    def operation(self):
        m = 1
        for el in self.data:
            m *= el
        return m

    @staticmethod
    def info(cls):
        return 'Multiplier class'


class Factory(ABC):
    @abstractmethod
    def create(self) -> Operation:
        pass

    def make(self) -> Operation:
        return self.create()


class SumFactory(Factory):
    def __init__(self, data: List[int]):
        self.data = data

    def create(self) -> Operation:
        return Adder(self.data)


class MulFactory(Factory):
    def __init__(self, data: List[int]):
        self.data = data

    def create(self) -> Operation:
        return Multiplier(self.data)


def calculation(f: Factory):
    operator = f.make()
    result = operator.operation()
    return result


if __name__ == '__main__':
    data = [1, 2, 3, 4, 5, 6]
    r = calculation(SumFactory(data))
    print(r)
    r = calculation(MulFactory(data))
    print(r)
