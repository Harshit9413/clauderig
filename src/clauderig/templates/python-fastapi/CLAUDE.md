# Project Rules — Python / FastAPI

## Stack
FastAPI, SQLAlchemy 2.x (async), Alembic, Pydantic v2, PostgreSQL, pytest-asyncio, httpx.

## Code Style
- PEP 8. Run `ruff check --fix` before every commit.
- Type-hint every parameter and return value — no bare untyped functions.
- No bare `except:` — catch specific exception types.
- All route handlers must be `async def`.

## File/Folder Conventions
```
app/
  routers/<resource>.py          — route handlers only (thin, < 10 lines each)
  services/<resource>_service.py — business logic and DB operations
  schemas/<resource>.py          — Pydantic request + response models
  models/<resource>.py           — SQLAlchemy ORM models
  dependencies.py                — shared Depends() factories (auth, db, pagination)
  database.py                    — engine and async session factory
  main.py                        — app creation, router mounts, lifespan
alembic/
  versions/                      — migration scripts
tests/
  test_<resource>.py             — mirrors app/ structure
```

## Always Do
- Prefix all API routes: `/api/v1/<resource>`
- Use Pydantic v2 models for all request/response data — never return raw dicts
- Separate input schemas (`UserCreate`) from output schemas (`UserResponse`)
- Use `model_config = ConfigDict(from_attributes=True)` on response schemas
- Use `Depends(get_db)` to inject `AsyncSession` into route handlers
- Use `selectinload()` / `joinedload()` to avoid N+1 queries
- Use `lifespan` context manager for startup/shutdown — not `@app.on_event`

## Never Do
- No DB queries in route handlers — service layer owns the DB
- No synchronous DB calls inside async route handlers
- No `session.commit()` inside a route — commit in the service
- No hard-coded secrets — use `pydantic-settings` with `.env`
- No `except Exception` — catch specific exception types
- No `import *`

## Testing
- Use `pytest-asyncio` with `httpx.AsyncClient` for endpoint tests
- Never mock the database — use a real test DB or SQLite in-memory
- Cover happy path + at least one error case per endpoint
- Run: `pytest` or `pytest -xvs tests/`

## Recommended MCP Servers
- **Postgres MCP** — query DB directly. Set `DATABASE_URL`.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — read/write project files. Pre-configured.
