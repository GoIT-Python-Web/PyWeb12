import logging

log_format = "%(asctime)s [%(levelname)s] %(funcName)15s %(lineno)5d - %(message)s"
LEVEL = logging.DEBUG

file_handler = logging.FileHandler("main.logs")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(log_format))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(logging.Formatter(log_format))


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
