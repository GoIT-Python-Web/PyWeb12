import logging
from random import randint

from psycopg2 import DatabaseError

from connection import create_connection


def alter_table(conn, sql_expression):
    c = conn.cursor()
    try:
        c.execute(sql_expression)
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_expression = "ALTER TABLE users ADD COLUMN phone VARCHAR(30);"

    try:
        with create_connection() as conn:
            if conn is not None:
                alter_table(conn, sql_expression)
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as e:
        logging.error(e)
