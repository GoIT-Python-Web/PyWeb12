"""
SQLAlchemy ORM Session
"""
import asyncio

import aiosqlite
from sqlalchemy import Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
DBSession = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

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


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_models()
    async with DBSession() as session:
        async with session.begin():
            new_user = User(fullname="Anton Petrenko")
            session.add(new_user)
            new_address = Address(email='apetrenko@meta.ua', user=new_user)
            session.add(new_address)
        # await session.commit()
            new_user = User(fullname="Sergiy Ponomarenko")
            session.add(new_user)
            new_address = Address(email='sponamar@meta.ua', user=new_user)
            session.add(new_address)
        # await session.commit()

        user = await session.execute(select(User))
        columns = ["id", "fullname"]
        db = [dict(zip(columns, (row.id, row.fullname))) for row in user.scalars()]
        print(db)

        address = await session.execute(select(Address).join(User))
        results = address.scalars()
        for a in results:
            print(a.id, a.email, a.user_id, a.user.fullname)


if __name__ == '__main__':
    asyncio.run(main())
