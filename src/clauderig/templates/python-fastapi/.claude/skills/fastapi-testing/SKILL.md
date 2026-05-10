---
name: fastapi-testing
description: FastAPI testing patterns using pytest, AsyncClient, and dependency overrides.
---

# FastAPI Testing Patterns

## Setup

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.db import get_session, Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(TEST_DATABASE_URL)

@pytest.fixture(autouse=True)
async def setup_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db(engine):
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session

@pytest.fixture
async def client(db: AsyncSession):
    app.dependency_overrides[get_session] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

## Basic Endpoint Test

```python
# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/users", json={"email": "alice@example.com", "password": "secret"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data
```

## Auth Test

```python
@pytest.mark.asyncio
async def test_protected_route_requires_auth(client):
    response = await client.get("/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_and_access_protected(client):
    await client.post("/users", json={"email": "bob@test.com", "password": "pass123"})

    token_resp = await client.post("/auth/token", data={"username": "bob@test.com", "password": "pass123"})
    token = token_resp.json()["access_token"]

    me_resp = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "bob@test.com"
```

## Dependency Override

```python
# Override auth for unit tests
from app.auth.dependencies import get_current_user
from app.models import User

def make_authenticated_client(app, db, user: User):
    app.dependency_overrides[get_session] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: user
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
```

## Pytest Config (pyproject.toml)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```
