from sqlalchemy.exc import SQLAlchemyError
from database.db import session
from database.models import User

if __name__ == '__main__':
    login = input('login: ')
    password = input('password: ')
    try:
        new_user = User(login=login, password=password)
        session.add(new_user)
        session.commit()
    except SQLAlchemyError as err:
        print(err)
