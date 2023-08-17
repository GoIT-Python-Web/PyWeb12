import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from main import app
from src.database.db import Base, get_db
from src.database.models import User
from src.services.auth import auth_service

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.sqlite"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
)

user = {
    "username": "deadpool",
    "email": "deadpool@example.com",
    "password": "123456789",
}

# @pytest.fixture(scope="module")
# def user():
#     return {"username": "deadpool", "email": "deadpool@example.com", "password": "123456789"}


@pytest.fixture(scope="module", autouse=True)
def init_models_fixture():
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            user_hash = auth_service.get_password_hash(user.get("password"))
            current_user = User(
                username=user.get("username"),
                email=user.get("email"),
                password=user_hash,
                confirmed=True,
                role="admin",
            )
            session.add(current_user)
            await session.commit()

    asyncio.run(init_models())


@pytest.fixture(scope="module")
def client():
    async def override_get_db():
        session = TestingSessionLocal()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def get_token(client):
    response = client.post(
        "/auth/login",
        data={
            "username": user.get("email"),
            "password": user.get("password"),
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    return data["access_token"]


@pytest_asyncio.fixture()
async def get_token_simple(client):
    access_token = await auth_service.create_access_token(
        data={"sub": user.get("email")}
    )
    return access_token
