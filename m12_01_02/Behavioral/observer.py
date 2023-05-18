from datetime import datetime


class Event:
    observers = []

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify(self, event_, data=None):
        for observer in self.observers:
            observer(event_, data)


def logger(event_, data):
    print(event_, data)


class FileLogger:
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, event_, data):
        with open(self.filename, 'a') as fd:
            fd.write(f"{datetime.now()}: [{event_}] - payload: {data}\n")


if __name__ == '__main__':
    event = Event()
    event.register(logger)
    f = FileLogger('app.logs')
    event.register(f)

    for tick in range(3):
        event.notify('TICK', tick)

    event.notify('ERROR', 'Sometime it happens!')
    event.unregister(f)

    for tick in range(3):
        event.notify('TICK', tick)
