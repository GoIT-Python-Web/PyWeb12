"""
SQLAlchemy Core
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select

engine = create_engine("sqlite:///:memory:", echo=True)

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('fullname', String)
              )

addresses = Table('addresses', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('email', String, nullable=False),
                  Column('user_id', Integer, ForeignKey('users.id'))
                  )

metadata.create_all(engine)


if __name__ == '__main__':
    with engine.connect() as conn:
        insert_user = users.insert().values(fullname="Anton Petrenko")
        print(str(insert_user))
        result = conn.execute(insert_user)
        print(result.lastrowid)
        # -----
        insert_user = users.insert().values(fullname="Єгор")
        print(str(insert_user))
        result = conn.execute(insert_user)
        print(result.lastrowid)
        # -----
        get_users = select(users)
        result = conn.execute(get_users)
        for row in result:
            print(row)

        insert_address = addresses.insert().values(email='egor@meta.ua', user_id=result.lastrowid)
        conn.execute(insert_address)
        insert_address = addresses.insert().values(email='apetrenko@meta.ua', user_id=1)
        conn.execute(insert_address)

        get_adr = select(addresses)
        result = conn.execute(get_adr)
        for row in result:
            print(row)

        custom_select = select(addresses.c.email, users.c.fullname).join(users)
        result = conn.execute(custom_select)
        for row in result:
            print(row)
