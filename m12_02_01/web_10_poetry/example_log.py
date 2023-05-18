from logger import get_logger

my_logger = get_logger(__file__)


def baz(num: int):
    result = num**2
    my_logger.debug(f"num: {num}, result = num ** 2: {result}")
    return result


if __name__ == "__main__":
    baz(5)
    my_logger.warning("This is a warning!")
    my_logger.error("Bababdum!")
