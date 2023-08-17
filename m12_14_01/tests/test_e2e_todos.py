from unittest.mock import MagicMock, patch, AsyncMock

import pytest
import pytest_asyncio

from src.services.auth import auth_service


def test_get_todos(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        response = client.get("api/todos", headers={"Authorization": f"Bearer {get_token}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list


# @pytest.mark.asyncio
def test_get_todos_simple(client, get_token_simple, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        response = client.get("api/todos", headers={"Authorization": f"Bearer {get_token_simple}"})
        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list


def test_get_todo(client, get_token, monkeypatch):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        response = client.get("api/todos/1", headers={"Authorization": f"Bearer {get_token}"})
        assert response.status_code == 404, response.text
        data = response.json()
        assert "detail" in data


def test_create_todo(client, get_token):
    with patch.object(auth_service, "cache") as redis_mock:
        redis_mock.get.return_value = None
        response = client.post("api/todos/", headers={"Authorization": f"Bearer {get_token}"}, json={
            "title": "Test",
            "description": "Test description"
        })
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["title"] == "Test"
