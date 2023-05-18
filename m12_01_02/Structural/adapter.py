class System:
    def execute(self, value_one, value_two, ops):
        if ops == 'add':
            return value_one + value_two
        elif ops == 'sub':
            return value_one - value_two
        else:
            raise ValueError('Unknown operation')


class NewSystem:
    def perform_execute(self, ops, value_one, value_two):
        if ops == '+':
            return value_one + value_two
        elif ops == '-':
            return value_one - value_two
        else:
            raise ValueError('Unknown operation')


class Adapter:
    def __init__(self, adapted):
        self.adapted = adapted

    def perform_execute(self, ops, value_one, value_two):
        if ops == '+':
            return self.adapted.execute(value_one, value_two, 'add')
        elif ops == '-':
            return self.adapted.execute(value_one, value_two, 'sub')
        else:
            raise ValueError('Unknown operation')


if __name__ == '__main__':
    res = NewSystem()
    r = res.perform_execute('+', 2, 2)
    print(r)

    res = Adapter(System())

    r = res.perform_execute('+', 2, 2)
    print(r)
