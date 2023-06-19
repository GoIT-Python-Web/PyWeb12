"""
SQLAlchemy ORM Session
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine("sqlite:///:memory:", echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    fullname = Column('fullname', String)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    user = relationship('User')


Base.metadata.create_all(engine)


if __name__ == '__main__':
    new_user = User(fullname="Anton Petrenko")
    session.add(new_user)
    new_address = Address(email='apetrenko@meta.ua', user=new_user)
    session.add(new_address)
    session.commit()

    user = session.query(User).first()
    print(user.id, user.fullname)

    new_address = session.query(Address).first()
    print(new_address.id, new_address.email, new_address.user_id, new_address.user.fullname)
    session.close()
