import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(funcName)15s %(lineno)5d - %(message)s"
)

# print a log message to the console.


def baz(num: int):
    result = num**2
    logging.debug(f"num: {num}, result = num ** 2: {result}")
    return result


if __name__ == "__main__":
    baz(5)
    logging.warning("This is a warning!")
