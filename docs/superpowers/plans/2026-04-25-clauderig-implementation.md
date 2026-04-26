# clauderig Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `clauderig` — a Python CLI (`claude-setup` command) that copies a stack-specific `.claude/` folder into any project, with pre-configured MCP servers and auto-lint hooks.

**Architecture:** Three thin Python modules (`cli.py`, `installer.py`, `analyzer.py`) plus five template trees under `src/clauderig/templates/`. The CLI delegates all file work to `installer.py`; `analyzer.py` is pure-read helpers with no side effects.

**Tech Stack:** Python 3.10+, typer>=0.12, rich>=13.0, pytest>=8.0, setuptools>=68

---

## File Map

| File | Purpose |
|---|---|
| `pyproject.toml` | Package config, entry point `claude-setup`, dev deps |
| `MANIFEST.in` | Force hidden `.claude/` dirs into sdist/wheel |
| `src/clauderig/__init__.py` | `__version__ = "0.1.0"` |
| `src/clauderig/__main__.py` | `python -m clauderig` entry |
| `src/clauderig/cli.py` | typer app: `init`, `list`, `version` |
| `src/clauderig/installer.py` | `install()`, `InstallResult`, `check_prerequisites()` |
| `src/clauderig/analyzer.py` | `detect_stack(path) -> str \| None` |
| `src/clauderig/templates/<stack>/.claude/` | Five template trees (see tasks 3–7) |
| `tests/test_cli.py` | CliRunner smoke tests |
| `tests/test_installer.py` | Parametrized install tests for all 5 stacks |
| `tests/test_analyzer.py` | Marker-file detection tests |
| `.github/workflows/test.yml` | CI: pytest on Python 3.10/3.11/3.12 |
| `README.md` | Product page |

---

## Task 1: Project Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `MANIFEST.in`
- Create: `LICENSE`
- Create: `.gitignore`
- Create: `src/clauderig/__init__.py`
- Create: `src/clauderig/__main__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create directory structure**

```bash
cd /Users/vishaljangid/learning/harshit/claude_setup_cli
mkdir -p src/clauderig/templates tests
```

- [ ] **Step 2: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "clauderig"
version = "0.1.0"
description = "Bootstrap a production-grade .claude/ setup into any project, instantly."
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.10"
authors = [{ name = "Your Name" }]
keywords = ["claude", "claude-code", "cli", "scaffold", "developer-tools"]
classifiers = [
  "Development Status :: 4 - Beta",
  "Environment :: Console",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
]
dependencies = ["typer>=0.12", "rich>=13.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "build>=1.0", "twine>=5.0"]

[project.scripts]
claude-setup = "clauderig.cli:app"

[project.urls]
Homepage = "https://github.com/yourusername/clauderig"
Repository = "https://github.com/yourusername/clauderig"
Issues = "https://github.com/yourusername/clauderig/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
clauderig = [
  "templates/**/*",
  "templates/**/.claude/**/*",
  "templates/**/.claude/*",
]
```

- [ ] **Step 3: Create `MANIFEST.in`**

```
recursive-include src/clauderig/templates *
global-exclude *.pyc
global-exclude __pycache__
```

- [ ] **Step 4: Create `LICENSE`**

```
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 5: Create `.gitignore`**

```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
*.egg
.pytest_cache/
.coverage
htmlcov/
*.whl
```

- [ ] **Step 6: Create `src/clauderig/__init__.py`**

```python
__version__ = "0.1.0"
```

- [ ] **Step 7: Create `src/clauderig/__main__.py`**

```python
from clauderig.cli import app

if __name__ == "__main__":
    app()
```

- [ ] **Step 8: Create `tests/__init__.py`**

```python
```

- [ ] **Step 9: Install in editable mode**

```bash
pip install -e ".[dev]"
```

Expected: installation completes, `claude-setup --help` prints the help text.

```bash
claude-setup --help
```

- [ ] **Step 10: Commit**

```bash
git add pyproject.toml MANIFEST.in LICENSE .gitignore src/ tests/
git commit -m "chore: project scaffold"
```

---

## Task 2: analyzer.py (TDD)

**Files:**
- Create: `src/clauderig/analyzer.py`
- Create: `tests/test_analyzer.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_analyzer.py`:

```python
import json
from pathlib import Path
import pytest
from clauderig.analyzer import detect_stack


def test_detect_django(tmp_path):
    (tmp_path / "manage.py").write_text("# django")
    assert detect_stack(tmp_path) == "python-django"


def test_detect_fastapi_via_requirements(tmp_path):
    (tmp_path / "requirements.txt").write_text("fastapi>=0.100\nuvicorn\n")
    assert detect_stack(tmp_path) == "python-fastapi"


def test_detect_fastapi_via_pyproject(tmp_path):
    (tmp_path / "pyproject.toml").write_text(
        '[tool.poetry.dependencies]\nfastapi = "*"\n'
    )
    assert detect_stack(tmp_path) == "python-fastapi"


def test_detect_django_via_requirements(tmp_path):
    (tmp_path / "requirements.txt").write_text("django>=4.0\ndjangorestframework\n")
    assert detect_stack(tmp_path) == "python-django"


def test_detect_php(tmp_path):
    (tmp_path / "composer.json").write_text('{"require": {}}')
    assert detect_stack(tmp_path) == "php"


def test_detect_react_web(tmp_path):
    pkg = {"dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    assert detect_stack(tmp_path) == "react-web"


def test_detect_react_native(tmp_path):
    (tmp_path / "app.json").write_text(json.dumps({"expo": {"name": "MyApp"}}))
    assert detect_stack(tmp_path) == "react-native"


def test_detect_unknown(tmp_path):
    assert detect_stack(tmp_path) is None


def test_django_manage_py_beats_requirements(tmp_path):
    (tmp_path / "manage.py").write_text("# django")
    (tmp_path / "requirements.txt").write_text("fastapi\n")
    assert detect_stack(tmp_path) == "python-django"


def test_react_native_app_json_beats_package_json(tmp_path):
    (tmp_path / "app.json").write_text(json.dumps({"expo": {"name": "App"}}))
    pkg = {"dependencies": {"react": "^18.0.0"}}
    (tmp_path / "package.json").write_text(json.dumps(pkg))
    assert detect_stack(tmp_path) == "react-native"
```

- [ ] **Step 2: Run tests — expect failure**

```bash
pytest tests/test_analyzer.py -v
```

Expected: `ImportError: cannot import name 'detect_stack'`

- [ ] **Step 3: Create `src/clauderig/analyzer.py`**

```python
from __future__ import annotations
import json
from pathlib import Path


def detect_stack(path: Path) -> str | None:
    """Return one of the five stack keys or None, based on marker files."""
    # Django: manage.py is definitive
    if (path / "manage.py").exists():
        return "python-django"

    # React Native: app.json with expo key
    app_json = path / "app.json"
    if app_json.exists():
        try:
            data = json.loads(app_json.read_text())
            if "expo" in data:
                return "react-native"
        except (json.JSONDecodeError, OSError):
            pass

    # React Web: package.json with react dependency
    pkg_json = path / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "react" in deps:
                return "react-web"
        except (json.JSONDecodeError, OSError):
            pass

    # PHP: composer.json
    if (path / "composer.json").exists():
        return "php"

    # Python: requirements.txt or pyproject.toml
    for filename in ("requirements.txt", "pyproject.toml"):
        marker = path / filename
        if marker.exists():
            try:
                content = marker.read_text().lower()
                if "fastapi" in content:
                    return "python-fastapi"
                if "django" in content:
                    return "python-django"
            except OSError:
                pass

    return None
```

- [ ] **Step 4: Run tests — expect all pass**

```bash
pytest tests/test_analyzer.py -v
```

Expected: 10 tests, all PASSED.

- [ ] **Step 5: Commit**

```bash
git add src/clauderig/analyzer.py tests/test_analyzer.py
git commit -m "feat: add stack auto-detection (analyzer.py)"
```

---

## Task 3: python-fastapi Template

**Files to create under `src/clauderig/templates/python-fastapi/.claude/`:**
- `settings.json`
- `CLAUDE.md`
- `commands/claude-fit.md`
- `commands/add-endpoint.md`
- `commands/add-test.md`
- `commands/review.md`
- `commands/db-migration.md`
- `skills/fastapi-patterns/SKILL.md`
- `skills/pydantic-models/SKILL.md`
- `skills/async-db/SKILL.md`
- `hooks/post-edit-lint.sh`
- `hooks/setup-mcps.sh`
- `rules/coding-standards.md`

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p src/clauderig/templates/python-fastapi/.claude/{commands,skills/fastapi-patterns,skills/pydantic-models,skills/async-db,hooks,rules}
```

- [ ] **Step 2: Create `settings.json`**

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(pytest:*)"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)", "Read(.env)", "Read(**/secrets/**)", "Read(**/.git/**)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/post-edit-lint.sh" }]
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

- [ ] **Step 3: Create `CLAUDE.md`**

```markdown
# Project Rules — FastAPI

## Stack
Python 3.10+, FastAPI, Pydantic v2, SQLAlchemy 2.x async, Alembic, pytest + httpx.

## Code Style
- PEP 8. Use `ruff` for linting (`ruff check --fix`).
- All functions must have type hints and return type declarations.
- No bare `except:` — always catch specific exception types.

## File/Folder Conventions
- Routers → `app/routers/<resource>.py`
- Pydantic schemas → `app/schemas/<resource>.py`
- SQLAlchemy models → `app/models/<resource>.py`
- Business logic → `app/services/<resource>_service.py`
- DB session/engine → `app/database.py`
- Shared dependencies → `app/dependencies.py`
- Entry point → `app/main.py`

## Always Do
- Use `async def` for all route handlers.
- Return Pydantic `response_model`, never raw dicts.
- Use `Depends()` for DB sessions and auth.
- Prefix routers: `/api/v1/<resource>`.
- Separate request schemas (input) from response schemas (output).

## Never Do
- No business logic in route handlers.
- No `.env` files committed.
- No `import *`.
- No `session.commit()` inside a route — service layer owns commits.

## Testing
- Tests in `tests/`, mirroring `app/` structure.
- Use `pytest-asyncio` + `httpx.AsyncClient` for endpoint tests.
- Run: `pytest -xvs`

## Recommended MCP Servers
- **Postgres MCP** — query DB from Claude. Needs: `DATABASE_URL` env var.
- **GitHub MCP** — browse issues/PRs. Needs: `GITHUB_TOKEN` env var.
- **Filesystem MCP** — read/write project files. Pre-configured.

Run `.claude/hooks/setup-mcps.sh` to install npm prerequisites.
```

- [ ] **Step 4: Create `commands/claude-fit.md`**

```markdown
---
name: claude-fit
description: Scan this FastAPI project and enhance .claude/ with project-specific skills, commands, and context.
---

# /claude-fit — FastAPI Project Scanner

Follow every step in order. Do not skip steps.

## Step 1: Inventory Dependency Files

Read these files if they exist (use the Read tool):
- `requirements.txt`, `pyproject.toml`, `Pipfile`, `poetry.lock`

Extract the full list of packages. Note these signals:
- `sqlalchemy` or `sqlmodel` → propose `sqlalchemy-patterns` skill
- `redis` or `aioredis` → propose `redis-caching` skill + Redis MCP note in CLAUDE.md
- `celery` → propose `celery-tasks` skill
- `alembic` → check if `db-migration` command already exists; if not, propose adding it
- `boto3` or `aiobotocore` → propose `s3-storage` skill
- `stripe` → propose `stripe-integration` skill
- `python-jose` or `authlib` → propose `auth-patterns` skill
- `sentry-sdk` → propose CLAUDE.md note
- `elasticsearch-py` → propose Elasticsearch MCP note

## Step 2: Inventory Project Structure

List files in the project root. Then read:
- `app/main.py` or `main.py`
- Contents of `app/routers/` if present
- Contents of `app/models/` if present
- Contents of `tests/` if present

Detect:
- Folder structure (routers per resource? per feature? versioned?)
- ORM in use (SQLAlchemy, SQLModel, Tortoise?)
- Auth approach (JWT, OAuth2, API keys?)
- Test runner command (check `pyproject.toml [tool.pytest]` or `pytest.ini`)

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`. Do not propose anything already present.

## Step 4: Present Checklist

Show the user a numbered list:

```
Proposed additions for this project:

1. Skill: sqlalchemy-patterns — detected SQLAlchemy in requirements.txt
2. Command: run-tests — detected pytest, command is `pytest -xvs`
3. CLAUDE.md update: Redis caching note (detected redis package)
...

Which would you like to add? (comma-separated numbers, or "all", or "none")
```

Wait for response before continuing.

## Step 5: Create Approved Files

For each approved skill, create `.claude/skills/<name>/SKILL.md`:
```
---
name: <name>
description: <one line>
---

# <Title>

<50-150 lines of real, useful guidance>
```

For each approved command, create `.claude/commands/<name>.md`:
```
---
name: <name>
description: <one line>
---

# /<name>

<Clear instructions Claude follows when this command is invoked>
```

For CLAUDE.md updates: append a new section, never delete existing content.

## Step 6: Update CLAUDE.md with Project Context

Append a `## Project-Specific Context` section to `.claude/CLAUDE.md`:

```markdown
## Project-Specific Context (auto-discovered by /claude-fit on YYYY-MM-DD)

- **Tests:** `<exact test command>` — `<test runner details>`
- **Routers:** `<path pattern>` — `<organization style>`
- **Models:** `<ORM name>`, session via `<module path>`
- **Auth:** `<approach>`, middleware in `<path>`
- **Recommended MCPs:** `<list with reason>`
```
```

- [ ] **Step 5: Create `commands/add-endpoint.md`**

```markdown
---
name: add-endpoint
description: Add a new FastAPI endpoint with router, schema, service, and test.
---

# /add-endpoint

Ask the user:
1. What resource? (e.g., users, products, orders)
2. HTTP method? (GET / POST / PUT / PATCH / DELETE)
3. What does it do?
4. Does it need authentication?

Then create (or add to existing files):
- `app/routers/<resource>.py` — route handler only, calls service
- `app/schemas/<resource>.py` — `<Resource>Create` and `<Resource>Response` Pydantic models
- `app/services/<resource>_service.py` — business + DB logic
- `tests/test_<resource>.py` — at least one test using `httpx.AsyncClient`

Conventions:
- Response model uses `model_config = ConfigDict(from_attributes=True)`
- Route handler uses `db: AsyncSession = Depends(get_db)`
- Service receives `AsyncSession` in `__init__`

After creating: mount the router in `app/main.py` if it's new.
Run `pytest -xvs tests/test_<resource>.py` and show output.
```

- [ ] **Step 6: Create `commands/add-test.md`**

```markdown
---
name: add-test
description: Write a pytest test for an existing FastAPI endpoint or service function.
---

# /add-test

Ask the user:
1. What to test? (endpoint path or service function name)
2. What behavior should the test verify?
3. Does it need a real DB or can it be a unit test?

Then:
- Find the file to test
- Write a focused test using `pytest-asyncio` + `httpx.AsyncClient` for endpoints
- Use `pytest.mark.asyncio` decorator
- Mock external calls (email, S3) with `unittest.mock.patch`
- Name tests: `test_<what>_<expected_outcome>` (e.g., `test_create_user_returns_201`)

Run `pytest -xvs <test_file>::<test_name>` and show output.
```

- [ ] **Step 7: Create `commands/review.md`**

```markdown
---
name: review
description: Review current branch changes for code quality, security, and test coverage.
---

# /review

Run in order:

1. `git diff main...HEAD` — list changed files
2. For each changed Python file check:
   - Type hints on all functions
   - No business logic in route handlers
   - No bare `except:` clauses
   - No secrets or tokens logged
   - Pydantic models used for input validation
3. Check: do changed files have corresponding test updates?
4. Run `pytest -x` — report pass/fail
5. Run `ruff check .` — report issues

Summary format:
- ✓ What looks good
- ✗ Issues to fix before merging
- ⚠ Suggestions (not blockers)
```

- [ ] **Step 8: Create `commands/db-migration.md`**

```markdown
---
name: db-migration
description: Create and apply an Alembic database migration.
---

# /db-migration

Ask: what schema change are you making?

Then:
1. Read `app/models/` to understand current model state
2. `alembic revision --autogenerate -m "<description>"`
3. Read the generated migration in `alembic/versions/`
4. Show the user `upgrade()` and `downgrade()` functions — ask to confirm
5. If confirmed: `alembic upgrade head`
6. If the migration touches existing rows: warn about data migration strategy

Always verify: does `downgrade()` correctly reverse `upgrade()`?
```

- [ ] **Step 9: Create `skills/fastapi-patterns/SKILL.md`**

```markdown
---
name: fastapi-patterns
description: FastAPI patterns for routes, dependency injection, middleware, and error handling.
---

# FastAPI Patterns

## Router Organization

One file per resource. Mount all routers in `app/main.py`.

```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserService(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).create(payload)
```

## Shared Dependencies

```python
# app/dependencies.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_db
from app.services.auth_service import AuthService

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    user = await AuthService(db).verify_token(credentials.credentials)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
```

## Global Error Handling

```python
# in app/main.py
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

## Lifespan (use this, not deprecated on_event)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
```

## Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/notify")
async def notify(bg: BackgroundTasks, email: str):
    bg.add_task(send_email, email)
    return {"queued": True}
```

## Mounting Routers

```python
# app/main.py
from app.routers import users, products
app.include_router(users.router)
app.include_router(products.router)
```
```

- [ ] **Step 10: Create `skills/pydantic-models/SKILL.md`**

```markdown
---
name: pydantic-models
description: Pydantic v2 patterns for validation, serialization, and settings management.
---

# Pydantic v2 Models

## Separate Input and Output Schemas

```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)  # replaces orm_mode=True

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
```

## Settings

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    cors_origins: list[str] = []
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

## Field Constraints

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0, description="Price in USD")
    tags: list[str] = Field(default_factory=list)
```

## Cross-Field Validation

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start: datetime
    end: datetime

    @model_validator(mode="after")
    def end_after_start(self) -> "DateRange":
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
```

## Common Gotcha

Pydantic v2 replaces `class Config: orm_mode = True` with
`model_config = ConfigDict(from_attributes=True)`. The old style silently no-ops.
```

- [ ] **Step 11: Create `skills/async-db/SKILL.md`**

```markdown
---
name: async-db
description: SQLAlchemy 2.x async session, query, and transaction patterns.
---

# Async Database (SQLAlchemy 2.x)

## Setup

```python
# app/database.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## Model Definition (typed columns)

```python
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
```

## Service Pattern

```python
from sqlalchemy import select

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        user = User(email=data.email, name=data.name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
```

## Explicit Transactions

```python
async def transfer(self, from_id: int, to_id: int, amount: int):
    async with self.db.begin():
        sender = await self.get_by_id(from_id)
        receiver = await self.get_by_id(to_id)
        sender.balance -= amount
        receiver.balance += amount
        # auto-commit on context exit
```

## Prevent N+1 with selectinload

```python
from sqlalchemy.orm import selectinload

result = await self.db.execute(
    select(User).options(selectinload(User.posts))
)
```
```

- [ ] **Step 12: Create `hooks/post-edit-lint.sh`**

```bash
#!/usr/bin/env bash
ruff check --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
```

- [ ] **Step 13: Create `hooks/setup-mcps.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for FastAPI projects..."
echo ""
echo "→ @modelcontextprotocol/server-github"
npm install -g @modelcontextprotocol/server-github
echo "→ @modelcontextprotocol/server-filesystem"
npm install -g @modelcontextprotocol/server-filesystem
echo "→ @modelcontextprotocol/server-postgres"
npm install -g @modelcontextprotocol/server-postgres
echo ""
echo "Done. Set these environment variables:"
echo "  export GITHUB_TOKEN=your_token_here"
echo "  export DATABASE_URL=postgresql://user:pass@localhost:5432/dbname"
```

- [ ] **Step 14: Create `rules/coding-standards.md`**

```markdown
# FastAPI Coding Standards

## Do
- Type-hint every parameter and return value
- Use Pydantic v2 models for all request/response data
- Keep route handlers under 10 lines; delegate to services
- Write one test per endpoint behavior
- Use `ruff check --fix` before every commit
- Prefix all API routes: `/api/v1/<resource>`

## Don't
- Don't put DB queries in route handlers
- Don't return raw dicts from endpoints
- Don't catch broad exceptions (`except Exception`)
- Don't commit `.env` or secrets
- Don't use synchronous DB calls in async route handlers
- Don't skip writing tests for happy path + one error case
```

- [ ] **Step 15: Commit**

```bash
git add src/clauderig/templates/python-fastapi/
git commit -m "feat: add python-fastapi template"
```

---

## Task 4: python-django Template

**Files under `src/clauderig/templates/python-django/.claude/`:**
`settings.json`, `CLAUDE.md`, `commands/` (5 files), `skills/` (3 folders), `hooks/` (2 files), `rules/coding-standards.md`

- [ ] **Step 1: Create directory tree**

```bash
mkdir -p src/clauderig/templates/python-django/.claude/{commands,skills/django-orm,skills/django-views,skills/drf-serializers,hooks,rules}
```

- [ ] **Step 2: Create `settings.json`**

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(python manage.py test:*)"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)", "Read(.env)", "Read(**/secrets/**)", "Read(**/.git/**)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/post-edit-lint.sh" }]
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

- [ ] **Step 3: Create `CLAUDE.md`**

```markdown
# Project Rules — Django

## Stack
Django 4.x+, Django REST Framework, PostgreSQL, pytest-django.

## Code Style
- PEP 8. Run `ruff check --fix` before commits.
- All functions/methods need type hints.
- No bare `except:`.

## File/Folder Conventions
- Views → `app/views.py` or `app/views/<resource>.py`
- Models → `app/models.py` or `app/models/<resource>.py`
- Serializers → `app/serializers.py`
- URLs → `app/urls.py`, included in project `urls.py`
- Settings → `project/settings/base.py`, `local.py`, `production.py`

## Always Do
- Use `get_object_or_404()` for single-object lookups
- Use DRF serializers for all API input/output
- Add `__str__` to every model
- Use `select_related` / `prefetch_related` to avoid N+1 queries

## Never Do
- No raw SQL — use ORM or `Manager.raw()` only when necessary
- No logic in templates
- No hard-coded settings — use `django.conf.settings`
- No `DEBUG=True` in production settings

## Testing
- Use `pytest-django` with `@pytest.mark.django_db`
- Use `APIClient` for endpoint tests
- Run: `python manage.py test` or `pytest`

## Recommended MCP Servers
- **Postgres MCP** — query DB directly. Set `DATABASE_URL`.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — read/write project files. Pre-configured.
```

- [ ] **Step 4: Create the 5 command files**

`commands/claude-fit.md`:
```markdown
---
name: claude-fit
description: Scan this Django project and enhance .claude/ with project-specific skills, commands, and context.
---

# /claude-fit — Django Project Scanner

Follow every step in order.

## Step 1: Inventory Dependencies

Read `requirements.txt`, `pyproject.toml`, `Pipfile`. Note:
- `celery` → propose `celery-tasks` skill
- `redis` → propose `redis-caching` skill + Redis MCP note
- `boto3` → propose `s3-storage` skill
- `stripe` → propose `stripe-integration` skill
- `djangorestframework-simplejwt` → propose `jwt-auth` skill
- `sentry-sdk` → propose CLAUDE.md note
- `django-storages` → propose CLAUDE.md note

## Step 2: Inventory Project Structure

Read `manage.py`, project `settings/` folder, `urls.py`. List apps in `INSTALLED_APPS`.
For each app: list models, views, serializers if present.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Show numbered proposal list. Wait for user selection.

## Step 5: Create Approved Files

Follow YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with:
- Exact test command
- App structure
- Auth approach
- DB config (Postgres, SQLite?)
- Any non-standard patterns
```

`commands/add-view.md`:
```markdown
---
name: add-view
description: Add a new DRF API view with serializer, URL routing, and test.
---

# /add-view

Ask the user:
1. Resource name? (e.g., products)
2. View type? (APIView / ModelViewSet / GenericAPIView)
3. Which HTTP methods?
4. Auth required?

Create:
- View in `app/views.py` or `app/views/<resource>.py`
- Serializer in `app/serializers.py`
- URL pattern in `app/urls.py`
- Test in `tests/test_<resource>.py` using `APIClient`

Run `python manage.py test tests.test_<resource>` and show output.
```

`commands/add-model.md`:
```markdown
---
name: add-model
description: Add a new Django model with migration.
---

# /add-model

Ask:
1. Model name?
2. Fields? (name, type, constraints for each)
3. Relationships? (ForeignKey, M2M?)

Then:
1. Add model to `app/models.py`
2. Add `__str__` method
3. `python manage.py makemigrations`
4. Show migration file — ask to confirm
5. `python manage.py migrate`
6. Register in `app/admin.py`
```

`commands/run-migration.md`:
```markdown
---
name: run-migration
description: Create and apply a Django database migration.
---

# /run-migration

Ask: what schema change are you making?

Then:
1. Make the model change
2. `python manage.py makemigrations --name <description>`
3. Show generated migration — ask to confirm
4. `python manage.py migrate`
5. If data migration needed: warn and propose a `RunPython` step
```

`commands/review.md`:
```markdown
---
name: review
description: Review current branch changes for code quality, security, and test coverage.
---

# /review

Run in order:
1. `git diff main...HEAD` — list changed files
2. For each changed Python file: type hints, no raw SQL, no logic in views beyond delegation
3. N+1 check: any new querysets without `select_related`/`prefetch_related`?
4. Check: do changed files have test updates?
5. `python manage.py test` — report results
6. `ruff check .` — report issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
```

- [ ] **Step 5: Create the 3 skill files**

`skills/django-orm/SKILL.md`:
```markdown
---
name: django-orm
description: Django ORM patterns for queries, relationships, and avoiding N+1 problems.
---

# Django ORM Patterns

## Basic Queries

```python
# Get or 404
from django.shortcuts import get_object_or_404
user = get_object_or_404(User, pk=user_id)

# Filter
users = User.objects.filter(is_active=True).order_by("-created_at")

# Exists check (cheaper than count)
if User.objects.filter(email=email).exists():
    raise ValidationError("Email taken")
```

## Relationships

```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

## Avoid N+1

```python
# Bad — hits DB once per post
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # N queries

# Good — 2 queries total
posts = Post.objects.select_related("author").all()

# For M2M
posts = Post.objects.prefetch_related("tags").all()
```

## Custom Manager

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class User(models.Model):
    objects = models.Manager()
    active = ActiveManager()
```

## Transactions

```python
from django.db import transaction

@transaction.atomic
def transfer(from_user, to_user, amount):
    from_user.balance -= amount
    to_user.balance += amount
    from_user.save()
    to_user.save()
```

## Bulk Operations

```python
# Bulk create (single query)
User.objects.bulk_create([User(email=e) for e in emails])

# Bulk update
User.objects.filter(is_trial=True).update(plan="free")
```
```

`skills/django-views/SKILL.md`:
```markdown
---
name: django-views
description: DRF ViewSet, APIView, and permission patterns.
---

# DRF View Patterns

## ModelViewSet (most common)

```python
from rest_framework import viewsets, permissions
from app.models import Product
from app.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
```

Register in `urls.py`:
```python
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("products", ProductViewSet)
urlpatterns = [path("api/v1/", include(router.urls))]
```

## APIView (more control)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password updated"}, status=status.HTTP_200_OK)
```

## Custom Permissions

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

## Pagination

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```
```

`skills/drf-serializers/SKILL.md`:
```markdown
---
name: drf-serializers
description: DRF serializer patterns for validation, nested data, and write operations.
---

# DRF Serializer Patterns

## ModelSerializer

```python
from rest_framework import serializers
from app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]
        read_only_fields = ["id", "created_at"]
```

## Custom Validation

```python
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "name", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
```

## Nested Serializers

```python
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "city", "country"]

class UserDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "address"]
```

## SerializerMethodField

```python
class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
```

## Write Nested Data

```python
def create(self, validated_data):
    tags_data = validated_data.pop("tags", [])
    post = Post.objects.create(**validated_data)
    post.tags.set(tags_data)
    return post
```
```

- [ ] **Step 6: Create hooks and rules**

`hooks/post-edit-lint.sh`:
```bash
#!/usr/bin/env bash
ruff check --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
```

`hooks/setup-mcps.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for Django projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-postgres
echo ""
echo "Set: GITHUB_TOKEN and DATABASE_URL environment variables"
```

`rules/coding-standards.md`:
```markdown
# Django Coding Standards

## Do
- Add `__str__` to every model
- Use `select_related` / `prefetch_related` when traversing FK/M2M
- Use DRF serializers for all API I/O
- Keep views thin — business logic in services or model methods
- Use `get_object_or_404` for single-object lookups

## Don't
- No raw SQL queries (use ORM; `raw()` only as last resort)
- No logic in templates
- No `DEBUG=True` or `SECRET_KEY` hard-coded
- No skipping `makemigrations` before `migrate`
- No circular imports between apps
```

- [ ] **Step 7: Commit**

```bash
git add src/clauderig/templates/python-django/
git commit -m "feat: add python-django template"
```

---

## Task 5: PHP Template

**Files under `src/clauderig/templates/php/.claude/`:**

- [ ] **Step 1: Create directories**

```bash
mkdir -p src/clauderig/templates/php/.claude/{commands,skills/psr-standards,skills/composer-deps,hooks,rules}
```

- [ ] **Step 2: Create `settings.json`**

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(phpunit:*)", "Bash(php artisan:*)"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)", "Read(.env)", "Read(**/secrets/**)", "Read(**/.git/**)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/post-edit-lint.sh" }]
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${DATABASE_URL}"]
    }
  }
}
```

- [ ] **Step 3: Create `CLAUDE.md`**

```markdown
# Project Rules — PHP / Laravel

## Stack
PHP 8.1+, Laravel 10+, Eloquent ORM, PHPUnit.

## Code Style
- PSR-12 coding style. Run `php-cs-fixer fix` before commits.
- `declare(strict_types=1)` at top of every file.
- Use camelCase for methods/variables, PascalCase for classes.
- Return type declarations on all methods.

## File/Folder Conventions (Laravel)
- Controllers → `app/Http/Controllers/<Resource>Controller.php`
- Models → `app/Models/<Resource>.php`
- Migrations → `database/migrations/`
- Routes → `routes/api.php` for API, `routes/web.php` for web
- Services → `app/Services/<Resource>Service.php`
- Form Requests → `app/Http/Requests/<Resource>Request.php`

## Always Do
- Use Form Requests for validation (`php artisan make:request`)
- Use Eloquent models, never raw SQL
- Use Laravel CSRF protection in web routes
- Sanitize output to prevent XSS
- Return JSON from API controllers: `response()->json($data, $status)`

## Never Do
- No logic in controllers — use service classes
- No `DB::statement()` unless absolutely necessary
- No user input directly in queries
- No secrets in code — use `.env` + `config/`

## Testing
- PHPUnit feature tests in `tests/Feature/`
- Unit tests in `tests/Unit/`
- Run: `php artisan test` or `./vendor/bin/phpunit`
- Use factories: `User::factory()->create()`
- 85% coverage target

## Recommended MCP Servers
- **Postgres MCP** — query DB directly. Set `DATABASE_URL`.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
```

- [ ] **Step 4: Create the 4 command files**

`commands/claude-fit.md`:
```markdown
---
name: claude-fit
description: Scan this PHP project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — PHP Project Scanner

## Step 1: Inventory Dependencies

Read `composer.json` and `composer.lock`. Note:
- `laravel/sanctum` or `laravel/passport` → propose `api-auth` skill
- `predis/predis` → propose `redis-caching` skill + Redis MCP note
- `league/flysystem-aws-s3-v3` → propose `s3-storage` skill
- `spatie/laravel-permission` → propose `rbac-permissions` skill
- `stripe/stripe-php` → propose `stripe-integration` skill

## Step 2: Inventory Project Structure

List `app/Http/Controllers/`, `app/Models/`, `routes/`. Read `routes/api.php`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with test command, route structure, auth approach.
```

`commands/add-controller.md`:
```markdown
---
name: add-controller
description: Add a new Laravel API controller with routes, form request, and test.
---

# /add-controller

Ask:
1. Resource name? (e.g., Product)
2. Which methods? (index / show / store / update / destroy)
3. Auth required?

Then:
1. `php artisan make:controller <Resource>Controller --api`
2. `php artisan make:request Store<Resource>Request`
3. Add validation rules to the Form Request
4. Implement controller methods — each calls a service method
5. Register routes in `routes/api.php`
6. `php artisan make:test <Resource>ControllerTest`
7. Write feature tests using `$this->actingAs($user)->postJson(...)`

Run `php artisan test tests/Feature/<Resource>ControllerTest.php` and show output.
```

`commands/add-test.md`:
```markdown
---
name: add-test
description: Write a PHPUnit test for an existing controller endpoint or service method.
---

# /add-test

Ask:
1. What to test? (endpoint URL or class::method)
2. What behavior to verify?
3. Feature test (HTTP) or unit test?

Then:
- Feature tests use `$this->getJson()`, `$this->postJson()` etc.
- Mock external deps with `$this->mock(ServiceClass::class)`
- Use factories: `User::factory()->create()`
- Name: `test_<what>_<outcome>` (e.g., `test_create_product_returns_201`)

Run `php artisan test --filter=<test_name>` and show output.
```

`commands/review.md`:
```markdown
---
name: review
description: Review current branch for code quality, security, and test coverage.
---

# /review

Run in order:
1. `git diff main...HEAD`
2. For each PHP file: strict_types, type hints, no logic in controllers, no raw SQL
3. Security check: any `$request->input()` used directly in queries?
4. `php artisan test` — report results
5. `./vendor/bin/php-cs-fixer check .` — report style issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
```

- [ ] **Step 5: Create skill files**

`skills/psr-standards/SKILL.md`:
```markdown
---
name: psr-standards
description: PSR-1, PSR-4, PSR-7, and PSR-12 standards for PHP projects.
---

# PSR Standards

## PSR-12: Code Style

```php
<?php

declare(strict_types=1);

namespace App\Services;

class UserService
{
    public function __construct(
        private readonly UserRepository $repository,
    ) {}

    public function findById(int $id): ?User
    {
        return $this->repository->find($id);
    }

    public function create(array $data): User
    {
        return $this->repository->create($data);
    }
}
```

Key rules:
- 4-space indentation (no tabs)
- Opening brace on same line for classes and methods
- One blank line between methods
- `declare(strict_types=1)` after opening `<?php`

## PSR-4: Autoloading

```json
// composer.json
{
    "autoload": {
        "psr-4": {
            "App\\": "app/"
        }
    }
}
```

Run `composer dump-autoload` after adding new namespaces.

## Return Types

Always declare return types:

```php
public function getUser(int $id): User
public function findAll(): Collection
public function save(User $user): void
public function exists(string $email): bool
```

## Type Declarations

```php
// Property types (PHP 7.4+)
private string $name;
private ?int $age = null;
private readonly string $email;

// Constructor promotion (PHP 8.0+)
public function __construct(
    private string $name,
    private readonly int $id,
) {}
```

## Nullable vs Union Types

```php
// Nullable (can be null)
public function find(int $id): ?User { ... }

// Union (PHP 8.0+)
public function parse(string|int $input): string { ... }
```
```

`skills/composer-deps/SKILL.md`:
```markdown
---
name: composer-deps
description: Managing Composer dependencies, semantic versioning, and package security.
---

# Composer Dependency Management

## Version Constraints

```json
{
    "require": {
        "php": "^8.1",
        "laravel/framework": "^10.0",
        "guzzlehttp/guzzle": "^7.5"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "laravel/pint": "^1.0"
    }
}
```

- `^1.2.3` — compatible with 1.x, no breaking changes (recommended)
- `~1.2.3` — patch updates only (1.2.x)
- `1.2.3` — exact version (avoid unless necessary)

## Useful Commands

```bash
# Install (first time or after git pull)
composer install

# Add a package
composer require vendor/package

# Add dev-only package
composer require --dev vendor/package

# Update a specific package
composer update vendor/package

# Check for security advisories
composer audit

# Optimize autoloader for production
composer install --optimize-autoloader --no-dev
```

## Lock File

Always commit `composer.lock`. It guarantees reproducible installs.
Never edit it manually.

## Publishing a Private Package

```json
{
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/your-org/package"
        }
    ]
}
```

## Checking for Outdated Packages

```bash
composer outdated
composer outdated --direct  # only direct dependencies
```
```

- [ ] **Step 6: Create hooks and rules**

`hooks/post-edit-lint.sh`:
```bash
#!/usr/bin/env bash
php-cs-fixer fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
```

`hooks/setup-mcps.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for PHP projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-postgres
echo ""
echo "Set: GITHUB_TOKEN and DATABASE_URL environment variables"
```

`rules/coding-standards.md`:
```markdown
# PHP / Laravel Coding Standards

## Do
- `declare(strict_types=1)` at top of every file
- Use Form Requests for all validation
- Service classes for business logic; controllers only delegate
- Return type declarations on every method
- Use factories in tests, never hand-craft models

## Don't
- No `DB::raw()` with user input (SQL injection risk)
- No business logic in controllers or models
- No hard-coded credentials or `.env` values in code
- No `@` error suppression operator
- No skipping CSRF on web routes
```

- [ ] **Step 7: Commit**

```bash
git add src/clauderig/templates/php/
git commit -m "feat: add php template"
```

---

## Task 6: react-web Template

**Files under `src/clauderig/templates/react-web/.claude/`:**

- [ ] **Step 1: Create directories**

```bash
mkdir -p src/clauderig/templates/react-web/.claude/{commands,skills/react-hooks,skills/tailwind-patterns,skills/state-management,hooks,rules}
```

- [ ] **Step 2: Create `settings.json`**

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(npm test:*)", "Bash(npm run:*)"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)", "Read(.env)", "Read(**/secrets/**)", "Read(**/.git/**)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/post-edit-lint.sh" }]
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

- [ ] **Step 3: Create `CLAUDE.md`**

```markdown
# Project Rules — React (Web)

## Stack
React 18+, TypeScript, Vite or Next.js, Tailwind CSS.

## Code Style
- ESLint + Prettier. Run `npx eslint --fix` before commits.
- Use TypeScript strictly — no `any` without justification.
- Functional components only. No class components.
- File naming: `ComponentName.tsx`, hooks as `useHookName.ts`.

## File/Folder Conventions
- Components → `src/components/<ComponentName>/index.tsx`
- Pages/Views → `src/pages/` or `src/app/` (Next.js)
- Hooks → `src/hooks/use<Name>.ts`
- API calls → `src/api/<resource>.ts`
- Types → `src/types/<resource>.ts`
- Utils → `src/utils/<name>.ts`

## Always Do
- Use TypeScript interfaces for all props
- Extract data fetching logic into custom hooks
- Use `React.memo` for expensive render-heavy components
- Colocate component tests with the component
- Use Tailwind for styling — no inline styles

## Never Do
- No direct DOM manipulation (`document.getElementById`)
- No `useEffect` for derived state — use `useMemo`
- No prop drilling deeper than 2 levels — use context or state manager
- No API calls directly in components

## Testing
- Vitest + React Testing Library
- Run: `npm test`

## Recommended MCP Servers
- **Playwright MCP** — browser automation for testing. Pre-configured.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
```

- [ ] **Step 4: Create command files**

`commands/claude-fit.md`:
```markdown
---
name: claude-fit
description: Scan this React project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — React Project Scanner

## Step 1: Inventory Dependencies

Read `package.json`. Note:
- `zustand` or `@reduxjs/toolkit` → propose matching state-management skill update
- `react-query` or `@tanstack/react-query` → propose `react-query-patterns` skill
- `react-router-dom` → propose `routing-patterns` skill
- `axios` → propose `api-client` skill
- `@playwright/test` → propose E2E test command
- `framer-motion` → propose `animation-patterns` skill
- `next` → propose Next.js-specific skills

## Step 2: Inventory Project Structure

List `src/`. Check: components, hooks, pages, api, types folders. Read `src/App.tsx` or `src/main.tsx`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with: test command, folder structure, state management in use, API base URL pattern.
```

`commands/add-component.md`:
```markdown
---
name: add-component
description: Add a new React component with TypeScript props, styling, and test.
---

# /add-component

Ask:
1. Component name? (PascalCase)
2. What does it render?
3. What props does it accept?
4. Does it fetch data or receive it via props?

Create:
- `src/components/<Name>/index.tsx` — typed props interface, component
- `src/components/<Name>/<Name>.test.tsx` — at least: renders without crash + key behavior

Use Tailwind for styling. If it fetches data, extract into `src/hooks/use<Name>.ts`.

Run `npm test -- --run <Name>` and show output.
```

`commands/add-hook.md`:
```markdown
---
name: add-hook
description: Add a custom React hook for data fetching, state, or side effects.
---

# /add-hook

Ask:
1. Hook name? (use<Name>)
2. What does it do? (fetch data, manage form state, etc.)
3. What does it return?

Create `src/hooks/use<Name>.ts` with:
- TypeScript return type
- Loading, error states for data-fetching hooks
- Cleanup in `useEffect` where applicable

Write a test in `src/hooks/use<Name>.test.ts` using `renderHook` from `@testing-library/react`.

Run `npm test -- --run use<Name>` and show output.
```

`commands/review.md`:
```markdown
---
name: review
description: Review current branch for code quality, accessibility, and test coverage.
---

# /review

Run in order:
1. `git diff main...HEAD` — changed files
2. TypeScript check: `npx tsc --noEmit`
3. For each component: are props typed? any `any`? any direct DOM manipulation?
4. Check: do changed components have test updates?
5. `npm test` — report results
6. `npx eslint .` — report issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
```

- [ ] **Step 5: Create skill files**

`skills/react-hooks/SKILL.md`:
```markdown
---
name: react-hooks
description: React hook patterns for state, effects, data fetching, and performance.
---

# React Hook Patterns

## Data Fetching Hook

```typescript
// src/hooks/useUser.ts
import { useState, useEffect } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

export function useUser(userId: number) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then((r) => r.json())
      .then((data) => { if (!cancelled) setUser(data); })
      .catch((err) => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [userId]);

  return { user, loading, error };
}
```

## useMemo — Derived State

```typescript
const expensiveTotal = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]  // only recomputes when items changes
);
```

## useCallback — Stable References

```typescript
const handleSubmit = useCallback(
  (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(formData);
  },
  [formData, onSubmit]
);
```

## useRef — DOM + Mutable Values

```typescript
// Focus on mount
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => { inputRef.current?.focus(); }, []);

// Store interval without re-render
const intervalRef = useRef<NodeJS.Timeout | null>(null);
```

## Custom Form Hook

```typescript
export function useForm<T extends Record<string, unknown>>(initial: T) {
  const [values, setValues] = useState(initial);
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const reset = () => setValues(initial);
  return { values, onChange, reset };
}
```
```

`skills/tailwind-patterns/SKILL.md`:
```markdown
---
name: tailwind-patterns
description: Tailwind CSS patterns for layout, responsive design, and component styling.
---

# Tailwind CSS Patterns

## Responsive Layout

```tsx
// Mobile-first: stack on mobile, side-by-side on md+
<div className="flex flex-col md:flex-row gap-4">
  <aside className="w-full md:w-64 shrink-0">...</aside>
  <main className="flex-1 min-w-0">...</main>
</div>
```

## Card Component

```tsx
<div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
  <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
  <p className="mt-2 text-sm text-gray-500">{description}</p>
</div>
```

## Button Variants

```tsx
const base = "rounded-lg px-4 py-2 font-medium text-sm transition-colors focus-visible:outline-none focus-visible:ring-2";
const variants = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-100 text-gray-700 hover:bg-gray-200",
  danger: "bg-red-600 text-white hover:bg-red-700",
};
```

## Form Inputs

```tsx
<input
  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm
             placeholder:text-gray-400 focus:border-blue-500 focus:outline-none
             focus:ring-1 focus:ring-blue-500"
/>
```

## Conditional Classes (use clsx)

```typescript
import clsx from "clsx";

const className = clsx(
  "base-classes",
  isActive && "active-classes",
  isDisabled && "opacity-50 cursor-not-allowed"
);
```

## Dark Mode

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```
```

`skills/state-management/SKILL.md`:
```markdown
---
name: state-management
description: React state management patterns using Context, Zustand, and React Query.
---

# State Management Patterns

## Context for Auth/Theme (global, low-frequency)

```typescript
// src/context/AuthContext.tsx
import { createContext, useContext, useState, ReactNode } from "react";

interface AuthContextType {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  return (
    <AuthContext.Provider value={{ user, login: setUser, logout: () => setUser(null) }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be inside AuthProvider");
  return ctx;
}
```

## Zustand (client state, avoids prop drilling)

```typescript
// src/stores/cartStore.ts
import { create } from "zustand";

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  clear: () => void;
}

export const useCart = create<CartState>((set) => ({
  items: [],
  addItem: (item) => set((s) => ({ items: [...s.items, item] })),
  removeItem: (id) => set((s) => ({ items: s.items.filter((i) => i.id !== id) })),
  clear: () => set({ items: [] }),
}));
```

## React Query (server state)

```typescript
// src/hooks/useProducts.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

export function useProducts() {
  return useQuery({ queryKey: ["products"], queryFn: fetchProducts });
}

export function useCreateProduct() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: createProduct,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
}
```

## Rule of Thumb
- Local UI state → `useState`
- Derived values → `useMemo`
- Shared global state (low frequency) → Context
- Client state (medium frequency) → Zustand
- Server state (async) → React Query
```

- [ ] **Step 6: Create hooks and rules**

`hooks/post-edit-lint.sh`:
```bash
#!/usr/bin/env bash
npx eslint --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
```

`hooks/setup-mcps.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for React (Web) projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @playwright/mcp
echo ""
echo "Set: GITHUB_TOKEN environment variable"
echo "Playwright MCP is ready — no extra config needed"
```

`rules/coding-standards.md`:
```markdown
# React Web Coding Standards

## Do
- TypeScript for every file (.tsx / .ts)
- Props interfaces for every component
- Custom hooks for data fetching and complex state
- Tailwind for all styling
- Colocate tests with components

## Don't
- No `any` type without a comment explaining why
- No direct DOM manipulation
- No API calls inside JSX
- No useEffect for derived state (use useMemo)
- No prop drilling past 2 levels
```

- [ ] **Step 7: Commit**

```bash
git add src/clauderig/templates/react-web/
git commit -m "feat: add react-web template"
```

---

## Task 7: react-native Template

**Files under `src/clauderig/templates/react-native/.claude/`:**

- [ ] **Step 1: Create directories**

```bash
mkdir -p src/clauderig/templates/react-native/.claude/{commands,skills/expo-patterns,skills/navigation-setup,skills/native-modules,hooks,rules}
```

- [ ] **Step 2: Create `settings.json`**

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(npm test:*)", "Bash(npx expo:*)"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)", "Read(.env)", "Read(**/secrets/**)", "Read(**/.git/**)"]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{ "type": "command", "command": ".claude/hooks/post-edit-lint.sh" }]
      }
    ]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

- [ ] **Step 3: Create `CLAUDE.md`**

```markdown
# Project Rules — React Native

## Stack
React Native 0.73+, Expo SDK 50+, TypeScript, React Navigation v6.

## Code Style
- ESLint + Prettier. Run `npx eslint --fix` before commits.
- TypeScript strictly — no `any`.
- Functional components, hooks only.
- File naming: `ScreenName.tsx`, components as `ComponentName.tsx`.

## File/Folder Conventions
- Screens → `src/screens/<Name>Screen.tsx`
- Components → `src/components/<Name>.tsx`
- Navigation → `src/navigation/`
- Hooks → `src/hooks/use<Name>.ts`
- API calls → `src/api/<resource>.ts`
- Constants → `src/constants/`

## Always Do
- Use React Navigation for all navigation
- Handle safe-area insets via `SafeAreaView` or `useSafeAreaInsets`
- Test on both iOS and Android simulators
- Use platform-specific styles when needed (`Platform.OS`)

## Never Do
- No hard-coded colors — use a theme/constants file
- No inline styles — use `StyleSheet.create`
- No navigation imperative calls outside of screen components
- No bare `fetch` — wrap in a typed API client

## Testing
- Jest + React Native Testing Library
- Run: `npm test`

## Recommended MCP Servers
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
```

- [ ] **Step 4: Create command files**

`commands/claude-fit.md`:
```markdown
---
name: claude-fit
description: Scan this React Native project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — React Native Project Scanner

## Step 1: Inventory Dependencies

Read `package.json`. Note:
- `@react-native-async-storage/async-storage` → propose `storage-patterns` skill
- `react-native-reanimated` → propose `animation-patterns` skill
- `@tanstack/react-query` → propose `react-query-patterns` skill
- `zustand` → propose `state-management` skill
- `expo-notifications` → propose `push-notifications` skill
- `react-native-maps` → propose `maps-integration` skill

## Step 2: Inventory Project Structure

Read `app.json` or `app.config.js`. List `src/screens/`, `src/components/`, `src/navigation/`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with: Expo SDK version, navigation structure, state management, test command.
```

`commands/add-screen.md`:
```markdown
---
name: add-screen
description: Add a new React Native screen with navigation registration and test.
---

# /add-screen

Ask:
1. Screen name? (e.g., ProfileScreen)
2. What does it display?
3. What navigator does it belong to? (Stack / Tab / Drawer)
4. Props/route params it receives?

Create:
- `src/screens/<Name>Screen.tsx` — typed `RootStackParamList` params
- Register in the appropriate navigator in `src/navigation/`
- `src/screens/<Name>Screen.test.tsx` — at least: renders without crash

Use `StyleSheet.create` for styles. Use `useSafeAreaInsets` if needed.
Run `npm test -- --testPathPattern=<Name>Screen` and show output.
```

`commands/add-component.md`:
```markdown
---
name: add-component
description: Add a new React Native component with typed props and test.
---

# /add-component

Ask:
1. Component name?
2. What does it render?
3. What props?

Create:
- `src/components/<Name>.tsx` — typed props, `StyleSheet.create`
- `src/components/<Name>.test.tsx` — render test

Avoid: inline styles, platform-specific logic (extract to constants).
Run `npm test -- --testPathPattern=<Name>` and show output.
```

`commands/review.md`:
```markdown
---
name: review
description: Review current branch for RN code quality and test coverage.
---

# /review

1. `git diff main...HEAD`
2. For each changed file: typed props, StyleSheet.create used, no `any`, safe-area handled
3. Cross-platform: any iOS/Android specific code without `Platform.OS` guard?
4. `npm test` — report results
5. `npx eslint .` — report issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
```

- [ ] **Step 5: Create skill files**

`skills/expo-patterns/SKILL.md`:
```markdown
---
name: expo-patterns
description: Expo SDK patterns for config, assets, environment, and build.
---

# Expo Patterns

## app.config.js (dynamic config)

```javascript
// app.config.js
export default {
  expo: {
    name: "MyApp",
    slug: "my-app",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    splash: { image: "./assets/splash.png", resizeMode: "contain" },
    ios: { bundleIdentifier: "com.yourco.myapp", supportsTablet: false },
    android: { package: "com.yourco.myapp", adaptiveIcon: { foregroundImage: "./assets/adaptive-icon.png" } },
    extra: {
      apiUrl: process.env.API_URL,
      eas: { projectId: "your-project-id" },
    },
  },
};
```

## Environment Variables

```typescript
// src/constants/env.ts
import Constants from "expo-constants";

export const API_URL = Constants.expoConfig?.extra?.apiUrl as string;
```

Never put secrets in `app.config.js`. Use EAS Secrets for production.

## Expo Router (file-based)

If using Expo Router:
- Screens live in `app/` directory
- `app/(tabs)/index.tsx` → tab screen
- `app/[id].tsx` → dynamic route
- `app/_layout.tsx` → layout wrapper

## SecureStore (sensitive data)

```typescript
import * as SecureStore from "expo-secure-store";

await SecureStore.setItemAsync("authToken", token);
const token = await SecureStore.getItemAsync("authToken");
```

Never use AsyncStorage for tokens — use SecureStore.

## EAS Build

```bash
# Development build (for testing native modules)
eas build --profile development --platform ios

# Production
eas build --profile production --platform all
```
```

`skills/navigation-setup/SKILL.md`:
```markdown
---
name: navigation-setup
description: React Navigation v6 setup patterns for stacks, tabs, and deep linking.
---

# React Navigation v6

## Stack Navigator

```typescript
// src/navigation/AppNavigator.tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/HomeScreen";
import DetailScreen from "../screens/DetailScreen";

export type RootStackParamList = {
  Home: undefined;
  Detail: { id: number; title: string };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Detail" component={DetailScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

## Typed Navigation in Screens

```typescript
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../navigation/AppNavigator";

type Props = NativeStackScreenProps<RootStackParamList, "Detail">;

export default function DetailScreen({ route, navigation }: Props) {
  const { id, title } = route.params;
  return (
    <Button title="Go Back" onPress={() => navigation.goBack()} />
  );
}
```

## Tab Navigator

```typescript
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
const Tab = createBottomTabNavigator();

function TabNavigator() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
```

## useNavigation (inside deeply nested components)

```typescript
import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";

const nav = useNavigation<NativeStackNavigationProp<RootStackParamList>>();
nav.navigate("Detail", { id: 1, title: "Hello" });
```
```

`skills/native-modules/SKILL.md`:
```markdown
---
name: native-modules
description: Patterns for using native device APIs via Expo modules and bare React Native.
---

# Native Module Patterns

## Camera (expo-camera)

```typescript
import { CameraView, useCameraPermissions } from "expo-camera";

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();

  if (!permission?.granted) {
    return <Button title="Grant Camera Access" onPress={requestPermission} />;
  }

  return <CameraView style={{ flex: 1 }} facing="back" />;
}
```

## Location (expo-location)

```typescript
import * as Location from "expo-location";

async function getCurrentLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== "granted") return null;
  return Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
}
```

## Image Picker (expo-image-picker)

```typescript
import * as ImagePicker from "expo-image-picker";

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    aspect: [4, 3],
    quality: 0.8,
  });
  if (!result.canceled) return result.assets[0].uri;
  return null;
}
```

## Platform-Specific Code

```typescript
import { Platform, StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === "ios" ? 44 : 24,
    ...Platform.select({
      ios: { shadowColor: "#000", shadowOpacity: 0.1 },
      android: { elevation: 4 },
    }),
  },
});
```

## Permissions Pattern

Always check → request → handle denial gracefully. Never assume permission is granted.
```

- [ ] **Step 6: Create hooks and rules**

`hooks/post-edit-lint.sh`:
```bash
#!/usr/bin/env bash
npx eslint --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
```

`hooks/setup-mcps.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for React Native projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
echo ""
echo "Set: GITHUB_TOKEN environment variable"
```

`rules/coding-standards.md`:
```markdown
# React Native Coding Standards

## Do
- TypeScript for every file
- `StyleSheet.create` for all styles (enables optimization)
- `Platform.OS` / `Platform.select` for platform differences
- Handle permissions with graceful degradation
- Test on both iOS and Android

## Don't
- No inline styles objects (create new object each render)
- No AsyncStorage for sensitive data (use SecureStore)
- No hard-coded colors or spacing — use constants
- No navigation outside screen components
- No `any` type
```

- [ ] **Step 7: Commit**

```bash
git add src/clauderig/templates/react-native/
git commit -m "feat: add react-native template"
```

---

## Task 8: installer.py (TDD)

**Files:**
- Create: `tests/test_installer.py`
- Create: `src/clauderig/installer.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_installer.py`:

```python
import json
import os
from pathlib import Path
import pytest
from clauderig.installer import install, InstallResult

STACKS = ["python-fastapi", "python-django", "php", "react-web", "react-native"]


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_claude_dir(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    assert (tmp_path / ".claude").is_dir()


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_settings_json(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    settings = tmp_path / ".claude" / "settings.json"
    assert settings.exists()
    data = json.loads(settings.read_text())
    assert "permissions" in data
    assert "mcpServers" in data


@pytest.mark.parametrize("stack", STACKS)
def test_install_creates_claude_md(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    assert (tmp_path / ".claude" / "CLAUDE.md").exists()


@pytest.mark.parametrize("stack", STACKS)
def test_install_has_at_least_one_command(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    commands = list((tmp_path / ".claude" / "commands").glob("*.md"))
    assert len(commands) >= 1


@pytest.mark.parametrize("stack", STACKS)
def test_install_has_at_least_one_skill(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    skills = list((tmp_path / ".claude" / "skills").iterdir())
    assert len(skills) >= 1


@pytest.mark.parametrize("stack", STACKS)
def test_hooks_are_executable(tmp_path, stack):
    install(stack=stack, target=tmp_path, force=False, dry_run=False)
    hooks_dir = tmp_path / ".claude" / "hooks"
    for sh in hooks_dir.glob("*.sh"):
        assert os.access(sh, os.X_OK), f"{sh} is not executable"


def test_install_raises_on_existing_without_force(tmp_path):
    install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    with pytest.raises(FileExistsError, match="--force"):
        install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)


def test_install_force_overwrites(tmp_path):
    install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    install(stack="python-fastapi", target=tmp_path, force=True, dry_run=False)
    assert (tmp_path / ".claude").is_dir()


def test_dry_run_does_not_create_dir(tmp_path, capsys):
    result = install(stack="python-fastapi", target=tmp_path, force=False, dry_run=True)
    assert not (tmp_path / ".claude").exists()
    assert result.commands_count == 0


def test_install_result_counts(tmp_path):
    result = install(stack="python-fastapi", target=tmp_path, force=False, dry_run=False)
    assert isinstance(result, InstallResult)
    assert result.commands_count >= 1
    assert result.skills_count >= 1
    assert result.hooks_count >= 1
    assert len(result.mcps_configured) >= 1
    assert result.target_path == tmp_path / ".claude"


def test_invalid_stack_raises(tmp_path):
    with pytest.raises(ValueError, match="Unknown stack"):
        install(stack="not-a-stack", target=tmp_path, force=False, dry_run=False)
```

- [ ] **Step 2: Run tests — expect failure**

```bash
pytest tests/test_installer.py -v
```

Expected: `ImportError: cannot import name 'install'`

- [ ] **Step 3: Create `src/clauderig/installer.py`**

```python
from __future__ import annotations
import asyncio
import importlib.resources
import json
import shutil
import stat
from dataclasses import dataclass, field
from pathlib import Path


VALID_STACKS = frozenset({
    "python-fastapi",
    "python-django",
    "php",
    "react-web",
    "react-native",
})


@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path


def _count_dir(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for _ in path.iterdir())


def _get_mcps(settings_path: Path) -> list[str]:
    if not settings_path.exists():
        return []
    try:
        return list(json.loads(settings_path.read_text()).get("mcpServers", {}).keys())
    except (json.JSONDecodeError, OSError):
        return []


async def _probe_package(package: str) -> tuple[str, bool]:
    try:
        proc = await asyncio.create_subprocess_exec(
            "npx", "--yes", "--dry-run", package,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.wait_for(proc.wait(), timeout=8.0)
        return package, proc.returncode == 0
    except (asyncio.TimeoutError, FileNotFoundError, OSError):
        return package, False


async def check_prerequisites(mcps: list[str]) -> dict[str, bool]:
    """Concurrently probe whether MCP npm packages are resolvable."""
    results = await asyncio.gather(*[_probe_package(p) for p in mcps])
    return dict(results)


def install(stack: str, target: Path, force: bool, dry_run: bool) -> InstallResult:
    if stack not in VALID_STACKS:
        raise ValueError(f"Unknown stack: {stack!r}. Valid: {sorted(VALID_STACKS)}")

    dst = target / ".claude"

    if dst.exists() and not force:
        raise FileExistsError(
            f"`.claude/` already exists at {dst}. Use --force to overwrite."
        )

    pkg = importlib.resources.files("clauderig")
    src_traversable = pkg / "templates" / stack / ".claude"
    src_path = Path(str(src_traversable))

    if dry_run:
        for item in sorted(src_path.rglob("*")):
            if item.is_file():
                print(f"  would copy: {item.relative_to(src_path.parent.parent)}")
        return InstallResult(
            commands_count=0, skills_count=0, hooks_count=0,
            ruleset_count=0, mcps_configured=[], target_path=dst,
        )

    shutil.copytree(str(src_path), str(dst), dirs_exist_ok=force)

    hooks_dir = dst / "hooks"
    if hooks_dir.exists():
        for sh in hooks_dir.glob("*.sh"):
            sh.chmod(sh.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return InstallResult(
        commands_count=_count_dir(dst / "commands"),
        skills_count=_count_dir(dst / "skills"),
        hooks_count=_count_dir(dst / "hooks"),
        ruleset_count=_count_dir(dst / "rules"),
        mcps_configured=_get_mcps(dst / "settings.json"),
        target_path=dst,
    )
```

- [ ] **Step 4: Run tests — expect all pass**

```bash
pytest tests/test_installer.py -v
```

Expected: all tests PASSED.

- [ ] **Step 5: Commit**

```bash
git add src/clauderig/installer.py tests/test_installer.py
git commit -m "feat: add installer with InstallResult and async prerequisite check"
```

---

## Task 9: cli.py (TDD)

**Files:**
- Create: `tests/test_cli.py`
- Create: `src/clauderig/cli.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_cli.py`:

```python
from pathlib import Path
from typer.testing import CliRunner
from clauderig.cli import app
from clauderig import __version__

runner = CliRunner()


def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_list_shows_all_stacks():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "FastAPI" in result.output
    assert "Django" in result.output
    assert "Laravel" in result.output


def test_init_dry_run(tmp_path):
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path), "--dry-run",
    ])
    assert result.exit_code == 0
    assert not (tmp_path / ".claude").exists()


def test_init_noninteractive_fastapi(tmp_path):
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path),
    ])
    assert result.exit_code == 0
    assert (tmp_path / ".claude").is_dir()


def test_init_php_no_framework(tmp_path):
    result = runner.invoke(app, ["init", "--lang", "php", "--target", str(tmp_path)])
    assert result.exit_code == 0
    assert (tmp_path / ".claude").is_dir()


def test_init_invalid_framework_for_php():
    result = runner.invoke(app, ["init", "--lang", "php", "--framework", "fastapi", "--target", "/tmp"])
    assert result.exit_code == 1


def test_init_missing_framework_for_python():
    result = runner.invoke(app, ["init", "--lang", "python", "--target", "/tmp"])
    assert result.exit_code == 1


def test_init_existing_without_force(tmp_path):
    runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    result = runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    assert result.exit_code == 1
    assert "--force" in result.output


def test_init_force_overwrites(tmp_path):
    runner.invoke(app, ["init", "--lang", "python", "--framework", "fastapi", "--target", str(tmp_path)])
    result = runner.invoke(app, [
        "init", "--lang", "python", "--framework", "fastapi",
        "--target", str(tmp_path), "--force",
    ])
    assert result.exit_code == 0


def test_all_stacks_noninteractive(tmp_path):
    combos = [
        (["--lang", "python", "--framework", "django"], "python-django"),
        (["--lang", "react", "--framework", "reactjs"], "react-web"),
        (["--lang", "react", "--framework", "react-native"], "react-native"),
    ]
    for i, (flags, _) in enumerate(combos):
        target = tmp_path / str(i)
        target.mkdir()
        result = runner.invoke(app, ["init"] + flags + ["--target", str(target)])
        assert result.exit_code == 0, f"Failed: {flags}\n{result.output}"
```

- [ ] **Step 2: Run tests — expect failure**

```bash
pytest tests/test_cli.py -v
```

Expected: `ImportError: cannot import name 'app'`

- [ ] **Step 3: Create `src/clauderig/cli.py`**

```python
from __future__ import annotations
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from clauderig import __version__
from clauderig.installer import install

app = typer.Typer(
    help="Bootstrap a production-grade .claude/ setup into any project.",
    add_completion=False,
)
console = Console()

_LANG_FRAMEWORKS: dict[str, list[str]] = {
    "python": ["fastapi", "django"],
    "php": [],
    "react": ["reactjs", "react-native"],
}

_STACK_KEY: dict[str, str] = {
    "fastapi": "python-fastapi",
    "django": "python-django",
    "reactjs": "react-web",
    "react-native": "react-native",
}

_STACK_INFO: dict[str, dict[str, int]] = {
    "python-fastapi": {"commands": 5, "skills": 3, "hooks": 2, "mcps": 3},
    "python-django": {"commands": 5, "skills": 3, "hooks": 2, "mcps": 3},
    "php": {"commands": 4, "skills": 2, "hooks": 2, "mcps": 3},
    "react-web": {"commands": 4, "skills": 3, "hooks": 2, "mcps": 3},
    "react-native": {"commands": 4, "skills": 3, "hooks": 2, "mcps": 2},
}

_STACK_DISPLAY: dict[str, str] = {
    "python-fastapi": "Python → FastAPI",
    "python-django": "Python → Django",
    "php": "PHP (Laravel-friendly)",
    "react-web": "React → ReactJS (Web)",
    "react-native": "React → React Native",
}


def _resolve_stack(lang: str, framework: str | None) -> str:
    if lang == "php":
        if framework is not None:
            console.print(f"[red]Error:[/red] --lang php does not accept --framework. Got: {framework!r}")
            raise typer.Exit(1)
        return "php"
    if lang not in _LANG_FRAMEWORKS:
        console.print(f"[red]Error:[/red] Unknown --lang: {lang!r}. Choose: python, php, react")
        raise typer.Exit(1)
    valid = _LANG_FRAMEWORKS[lang]
    if framework not in valid:
        console.print(
            f"[red]Error:[/red] --lang {lang} requires --framework "
            f"{' or '.join(valid)}. Got: {framework!r}"
        )
        raise typer.Exit(1)
    return _STACK_KEY[framework]


@app.command()
def init(
    lang: Optional[str] = typer.Option(None, help="Language: python, php, react"),
    framework: Optional[str] = typer.Option(None, help="Framework: fastapi, django, reactjs, react-native"),
    target: Path = typer.Option(Path("."), help="Target directory"),
    force: bool = typer.Option(False, help="Overwrite existing .claude/"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print what would be copied"),
) -> None:
    """Bootstrap a .claude/ folder into a project."""
    interactive = lang is None

    if interactive:
        lang = typer.prompt("Primary language?", type=typer.Choice(["python", "php", "react"]))
        if lang in ("python", "react"):
            framework = typer.prompt("Framework?", type=typer.Choice(_LANG_FRAMEWORKS[lang]))
        target_str = typer.prompt("Target directory?", default=".")
        target = Path(target_str)

    stack = _resolve_stack(lang, framework)  # exits on invalid combo

    dst = target / ".claude"
    if dst.exists() and not force:
        if interactive:
            if not typer.confirm(".claude/ already exists. Overwrite?"):
                console.print("[yellow]Aborted.[/yellow]")
                raise typer.Exit(0)
            force = True
        else:
            console.print(f"[red]Error:[/red] `.claude/` already exists at {dst}. Use --force to overwrite.")
            raise typer.Exit(1)

    try:
        result = install(stack=stack, target=target, force=force, dry_run=dry_run)
    except (FileExistsError, PermissionError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1)

    if dry_run:
        return

    console.print(f"[green]✓[/green] Copied .claude/ to {result.target_path.resolve()}")
    console.print(
        f"[green]✓[/green] Installed: {result.commands_count} commands · "
        f"{result.skills_count} skills · {result.hooks_count} hooks · "
        f"{result.ruleset_count} ruleset"
    )
    if result.mcps_configured:
        console.print(f"[green]✓[/green] MCPs pre-configured: {', '.join(result.mcps_configured)}")
    console.print("[blue]→[/blue] Run `.claude/hooks/setup-mcps.sh` once to install MCP prerequisites")
    console.print("[blue]→[/blue] Run `claude` and try the /claude-fit slash command")


@app.command(name="list")
def list_stacks() -> None:
    """List supported stacks and what each ships."""
    table = Table(title="Supported Stacks", header_style="bold blue")
    table.add_column("Stack", style="cyan")
    table.add_column("Commands", justify="center")
    table.add_column("Skills", justify="center")
    table.add_column("Hooks", justify="center")
    table.add_column("MCPs", justify="center")

    for key, info in _STACK_INFO.items():
        table.add_row(
            _STACK_DISPLAY[key],
            str(info["commands"]),
            str(info["skills"]),
            str(info["hooks"]),
            str(info["mcps"]),
        )

    console.print(table)


@app.command()
def version() -> None:
    """Print the clauderig version."""
    console.print(f"clauderig {__version__}")
```

- [ ] **Step 4: Run tests — expect all pass**

```bash
pytest tests/test_cli.py -v
```

Expected: all tests PASSED.

- [ ] **Step 5: Run full test suite**

```bash
pytest -v --cov=clauderig --cov-report=term-missing
```

Expected: all tests pass, coverage ≥ 70%.

- [ ] **Step 6: Commit**

```bash
git add src/clauderig/cli.py tests/test_cli.py
git commit -m "feat: add CLI with init, list, version commands"
```

---

## Task 10: Smoke Test All Stacks

- [ ] **Step 1: Smoke test FastAPI**

```bash
claude-setup init --lang python --framework fastapi --target /tmp/smoke-fastapi
ls -la /tmp/smoke-fastapi/.claude
ls /tmp/smoke-fastapi/.claude/commands
ls /tmp/smoke-fastapi/.claude/skills
```

Expected: `.claude/` exists with `settings.json`, `CLAUDE.md`, `commands/`, `skills/`, `hooks/`, `rules/`.

- [ ] **Step 2: Smoke test Django**

```bash
claude-setup init --lang python --framework django --target /tmp/smoke-django
ls -la /tmp/smoke-django/.claude
```

Expected: same structure, `django` specific content in `CLAUDE.md`.

- [ ] **Step 3: Smoke test PHP**

```bash
claude-setup init --lang php --target /tmp/smoke-php
ls -la /tmp/smoke-php/.claude
```

- [ ] **Step 4: Smoke test React Web**

```bash
claude-setup init --lang react --framework reactjs --target /tmp/smoke-react-web
ls -la /tmp/smoke-react-web/.claude
```

- [ ] **Step 5: Smoke test React Native**

```bash
claude-setup init --lang react --framework react-native --target /tmp/smoke-react-native
ls -la /tmp/smoke-react-native/.claude
```

- [ ] **Step 6: Verify hooks are executable**

```bash
ls -la /tmp/smoke-fastapi/.claude/hooks/
```

Expected: `-rwxr-xr-x` permissions on `.sh` files.

- [ ] **Step 7: Smoke test `list` and `version`**

```bash
claude-setup list
claude-setup version
```

---

## Task 11: Build Wheel + Verify Template Inclusion

- [ ] **Step 1: Build**

```bash
pip install build
python -m build
```

Expected: `dist/clauderig-0.1.0-py3-none-any.whl` and `dist/clauderig-0.1.0.tar.gz`.

- [ ] **Step 2: Verify hidden `.claude` dirs are in the wheel**

```bash
unzip -l dist/clauderig-0.1.0-py3-none-any.whl | grep ".claude"
```

Expected: lines like `clauderig/templates/python-fastapi/.claude/settings.json`.

If NO `.claude` files appear, add to `MANIFEST.in`:
```
recursive-include src/clauderig/templates .claude
```
And re-run `python -m build`.

- [ ] **Step 3: Test wheel install in a temp venv**

```bash
python -m venv /tmp/testenv
/tmp/testenv/bin/pip install dist/clauderig-0.1.0-py3-none-any.whl
/tmp/testenv/bin/claude-setup init --lang python --framework fastapi --target /tmp/wheel-test
ls /tmp/wheel-test/.claude
```

Expected: `.claude/` folder created with full content. If `FileNotFoundError` for templates, the package-data glob needs fixing.

- [ ] **Step 4: Commit**

```bash
git add dist/ || true  # skip if .gitignored
git commit -m "chore: verify wheel build and template inclusion"
```

---

## Task 12: CI Workflow + README

- [ ] **Step 1: Create `.github/workflows/test.yml`**

```yaml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "${{ matrix.python }}"
      - run: pip install -e ".[dev]"
      - run: pytest -v --cov=clauderig
```

- [ ] **Step 2: Create `README.md`**

```markdown
# clauderig

Bootstrap a production-grade `.claude/` setup into any project — one command.

```bash
pipx install clauderig
cd my-project
claude-setup init
```

---

## What You Get

- **`settings.json`** — permissions, allowed commands, auto-lint hook, pre-configured MCP servers
- **`commands/`** — slash commands: `/claude-fit`, stack-specific add/review commands
- **`skills/`** — 2–3 skill folders with real guidance (not lorem ipsum)
- **`hooks/post-edit-lint.sh`** — auto-runs linter after every file edit
- **`hooks/setup-mcps.sh`** — one-shot MCP prerequisite installer
- **`rules/coding-standards.md`** — dos and don'ts for your stack

---

## Supported Stacks

| Stack | CLI flags | Commands | Skills | MCPs |
|---|---|---|---|---|
| Python → FastAPI | `--lang python --framework fastapi` | 5 | 3 | 3 |
| Python → Django | `--lang python --framework django` | 5 | 3 | 3 |
| PHP (Laravel) | `--lang php` | 4 | 2 | 3 |
| React → Web | `--lang react --framework reactjs` | 4 | 3 | 3 |
| React → Native | `--lang react --framework react-native` | 4 | 3 | 2 |

---

## Install

```bash
# Recommended (isolated environment)
pipx install clauderig

# Or via pip
pip install clauderig
```

Requires Python 3.10+.

---

## Usage

### Initialize a project

```bash
# Interactive
claude-setup init

# Non-interactive
claude-setup init --lang python --framework fastapi --target .
claude-setup init --lang php --target .
claude-setup init --lang react --framework reactjs --force
```

### List supported stacks

```bash
claude-setup list
```

### Check version

```bash
claude-setup version
```

---

## The `/claude-fit` Command

After `claude-setup init`, open your project in Claude Code and run `/claude-fit`.

Claude will:
1. Scan your dependency files (`requirements.txt`, `package.json`, `composer.json`, etc.)
2. Detect libraries you're actually using (SQLAlchemy, Redis, Stripe, etc.)
3. Propose new skills and commands tailored to your specific project
4. Update `CLAUDE.md` with discovered project context (test command, folder structure, auth approach)

This turns a generic `.claude/` setup into one that knows your exact project.

---

## MCP Servers

Each stack ships with pre-configured MCP servers in `settings.json`. Run the setup script once to install the prerequisites:

```bash
bash .claude/hooks/setup-mcps.sh
```

Then set the required environment variables (listed in the script output).

**All stacks:** GitHub MCP, Filesystem MCP  
**Python / PHP:** + PostgreSQL MCP  
**React Web:** + Playwright MCP  

---

## Contributing — Adding a New Stack

1. Create `src/clauderig/templates/<stack-name>/.claude/` with all required files
2. Add the stack key to `VALID_STACKS` in `installer.py`
3. Add the stack to `_STACK_INFO` and `_STACK_DISPLAY` in `cli.py`
4. Add detection logic to `analyzer.py`
5. Add parametrized tests in `test_installer.py`
6. Open a PR

---

## Decisions

- CLI command is `claude-setup`; package/import name is `clauderig`
- PHP has no sub-framework selection (single stack, Laravel-friendly)
- MCPs are pre-configured but not auto-installed — run `setup-mcps.sh` manually
- `--auto-detect` flag is stubbed but not exposed in v1

---

## License

MIT
```

- [ ] **Step 3: Commit**

```bash
git add .github/ README.md
git commit -m "chore: add CI workflow and README"
```

---

## 📦 Ship It — Commands to Run

### A. Final local verification

```bash
pytest -v --cov=clauderig
claude-setup init --lang python --framework fastapi --target /tmp/verify
ls -la /tmp/verify/.claude
claude-setup list
claude-setup version
```

### B. Push to GitHub

```bash
git init  # if not already done
git add .
git commit -m "Initial commit: clauderig v0.1.0"
gh repo create clauderig --public --source=. --remote=origin --push
git tag v0.1.0
git push origin v0.1.0
```

### C. Publish to PyPI (first time)

```bash
# 1. Register at https://pypi.org/account/register/
# 2. Enable 2FA at https://pypi.org/manage/account/
# 3. Create API token at https://pypi.org/manage/account/token/
# 4. Save to ~/.pypirc:
cat > ~/.pypirc <<'EOF'
[pypi]
  username = __token__
  password = pypi-AgEI...your-token-here
EOF
chmod 600 ~/.pypirc
```

Every release:

```bash
rm -rf dist/ build/ *.egg-info
python -m build
twine check dist/*
twine upload dist/*
```

Optional — test on TestPyPI first:

```bash
twine upload --repository testpypi dist/*
pipx install --index-url https://test.pypi.org/simple/ clauderig
```

### D. Teammates install

```bash
pipx install clauderig        # recommended
# or: pip install clauderig

cd ~/my-project
claude-setup init
claude                         # opens Claude Code
# then run: /claude-fit
```

### E. Future releases

```bash
# 1. Bump version in src/clauderig/__init__.py and pyproject.toml
git commit -am "Release v0.1.1"
git tag v0.1.1
git push && git push --tags
rm -rf dist/ build/ *.egg-info
python -m build
twine upload dist/*
```
```
