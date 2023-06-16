import logging

from psycopg2 import DatabaseError

from connection import create_connection
from insert import COUNT, fake


def update_table(conn, sql_expression):
    c = conn.cursor()
    try:
        for i in range(COUNT):
            c.execute(sql_expression, (fake.phone_number(), i + 1))
        conn.commit()
    except DatabaseError as e:
        logging.error(e)
        conn.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_expression = "UPDATE users SET phone = %s WHERE id = %s;"

    try:
        with create_connection() as conn:
            if conn is not None:
                update_table(conn, sql_expression)
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as e:
        logging.error(e)
