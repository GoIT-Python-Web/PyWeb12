class Greeting:
    def __init__(self, username):
        self.username = username

    def greet(self):
        return f"Hello Mr.(s) {self.username}"


class Decorator:
    def __init__(self, wrapper):
        self.wrapper = wrapper

    def greet(self):
        base = self.wrapper.greet()
        base = base.upper()
        return base


if __name__ == '__main__':
    msg = Decorator(Greeting('Tedim'))
    print(msg.greet())

