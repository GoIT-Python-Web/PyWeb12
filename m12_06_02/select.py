import logging

from psycopg2 import DatabaseError

from connection import create_connection


if __name__ == '__main__':
    sql_expression1 = "SELECT * FROM users WHERE id = %s;"
    sql_expression2 = """
        SELECT id, name, age 
        FROM users 
        WHERE age >=30
        ORDER BY age desc
        LIMIT 3;
        """

    try:
        with create_connection() as conn:
            if conn is not None:
                c = conn.cursor()
                try:
                    c.execute(sql_expression2)
                    result = c.fetchone()
                    print(result)
                    c.execute(sql_expression2)
                    c.execute(sql_expression2)
                    print(c.fetchall())
                except DatabaseError as e:
                    logging.error(e)
                finally:
                    c.close()
            else:
                print("Error! cannot create the database connection.")
    except RuntimeError as e:
        logging.error(e)
