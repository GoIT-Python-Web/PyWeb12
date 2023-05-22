from random import randint
from threading import Semaphore, Thread, RLock, current_thread, Lock
from time import sleep
import logging


class Logger:
    def __init__(self):
        self.active = []
        self.lock = RLock()

    def make_active(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug(f"Почав работу поток {name}. Зараз в пуле потоки: {self.active}")

    def make_inactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug(f"Закінчив работу поток {name}. Зараз в пуле потоки: {self.active}")


def worker(semaphore: Semaphore, pool: Logger):
    logging.debug(f'Wait...')
    with semaphore:
        name = current_thread().name
        pool.make_active(name)
        logging.debug(f'Got semaphore')
        sleep(randint(1, 3))
        pool.make_inactive(name)
    logging.debug(f'finished')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    semaphore = Semaphore(3)
    logger_pool = Logger()

    for i in range(12):
        th = Thread(target=worker, args=(semaphore, logger_pool))
        th.start()

