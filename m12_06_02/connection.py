import psycopg2
from contextlib import contextmanager
from psycopg2 import OperationalError


@contextmanager
def create_connection():
    try:
        conn = psycopg2.connect(host="localhost", database="test", user="postgres", password="567234")
        yield conn
        conn.close()
    except OperationalError as err:
        raise RuntimeError(f"Failed to connect: {err}")
