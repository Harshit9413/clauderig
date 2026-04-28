---
name: claude-fit
description: Deep-scan this Django project and rebuild .claude/ to be fully project-specific.
---

# /claude-fit

You are performing a **complete project analysis** to transform this `.claude/` folder from generic templates into a project-specific tool. Work through every phase completely without skipping.

---

## Phase 1: Project Discovery

Read every file below that exists (use the Read tool):

**Dependency files:**
`requirements.txt`, `requirements/base.txt`, `requirements/dev.txt`, `pyproject.toml`, `Pipfile`

**Django entry points:**
`manage.py`, `wsgi.py`, `asgi.py`

**Settings — read whichever exists:**
`settings.py`, `settings/base.py`, `settings/local.py`, `config/settings/base.py`, `<projectname>/settings.py`

**URL config:**
Root `urls.py`, then each `app/urls.py` found

**Installed apps — for each app in INSTALLED_APPS that is local (not django.* or third-party):**
- `<app>/models.py`
- `<app>/views.py` or `<app>/viewsets.py`
- `<app>/serializers.py` (if DRF)
- `<app>/urls.py`
- `<app>/admin.py`

**Tests:**
`pytest.ini`, `setup.cfg [tool:pytest]`, `pyproject.toml [tool.pytest]`, and up to 3 test files from `tests/` or per-app `tests/`

**Tooling:**
`Makefile`, `justfile`, `docker-compose.yml`, `.github/workflows/`

**Existing .claude/ content:**
`.claude/CLAUDE.md`, list all files in `.claude/skills/`, `.claude/commands/`, `.claude/rules/`, `.claude/memory/`

---

## Phase 2: Extract Project Context

Build this context map:

- **PROJECT_NAME** — Django project name (from `manage.py` or settings module)
- **PURPOSE** — 1–2 sentences from README or project description
- **PYTHON_VERSION** — from `pyproject.toml` or `.python-version`
- **LOCAL_APPS** — list of local Django apps (not django.* or third-party)
- **DEV_SERVER_CMD** — `python manage.py runserver` or `make dev` if Makefile exists
- **TEST_CMD** — `python manage.py test` or `pytest` (check if pytest-django is installed)
- **MIGRATE_CMD** — `python manage.py migrate`
- **MAKEMIGRATIONS_CMD** — `python manage.py makemigrations`
- **LINT_CMD** — ruff / flake8 / pylint, whatever is configured
- **FORMAT_CMD** — ruff format / black, whatever is configured
- **MODEL_NAMES** — all model class names found across all local apps
- **DATABASE** — PostgreSQL / SQLite / MySQL (from DATABASES setting)
- **AUTH_MODEL** — custom User model if `AUTH_USER_MODEL` is set, else `auth.User`
- **DRF** — yes/no (django-rest-framework in requirements)
- **AUTH_APPROACH** — JWT (simplejwt / djoser) / Session / Token / None
- **CACHE** — Redis / Memcached / LocMem / None (from CACHES setting)
- **QUEUE** — Celery / Django-Q / None
- **CHANNELS** — yes/no (django-channels in requirements)
- **EXTRA_LIBS** — all other non-standard detected libraries

---

## Phase 3: Fully Rewrite .claude/CLAUDE.md

**Replace** the entire contents of `.claude/CLAUDE.md`:

```
# Project Rules — [PROJECT_NAME]

## Stack
[Actual: Python X.Y, Django X.Y, DRF X.Y if present, database, test runner]

## Dev Commands
- Start:            [DEV_SERVER_CMD]
- Test:             [TEST_CMD]
- Migrate:          [MIGRATE_CMD]
- Make migrations:  [MAKEMIGRATIONS_CMD]
- Shell:            python manage.py shell
- Lint:             [LINT_CMD]
- Format:           [FORMAT_CMD]

## Apps
[LOCAL_APPS — one line per app with what it owns]

## Models
[MODEL_NAMES grouped by app — one line per model with key fields]

## Auth
Model: [AUTH_MODEL]
Approach: [AUTH_APPROACH — where tokens are issued, validated, what headers are expected]

## Database
[DATABASE]. ORM: Django ORM. Migrations: [MIGRATE_CMD].

## API Style
[REST via DRF ViewSets / APIView / Function-based views — derive from what's in the codebase]

## Code Style
[Detected linter/formatter. If none: PEP 8, 4 spaces, type hints encouraged]

## Always Do
[Derive from actual source patterns found]

## Never Do
[Derive from codebase conventions]

## Testing
[Exact test command, test file organization found, fixtures/factories in use]

## MCP Servers
[Postgres if DATABASES is postgres; Redis MCP if CACHE is Redis; GitHub MCP always]
```

---

## Phase 4: Create .claude/memory/ Files

### .claude/memory/project.md
```
---
type: project
updated: [today YYYY-MM-DD]
---
# [PROJECT_NAME]

[PURPOSE]

## Quick Reference
- Dev server: [DEV_SERVER_CMD]
- Tests:      [TEST_CMD]
- Database:   [DATABASE]
- Auth:       [AUTH_APPROACH]
- Cache:      [CACHE]

## Django Apps
[LOCAL_APPS — name, what it owns, key models]

## Custom User Model
[AUTH_MODEL — fields, manager, if customized]

## Key Files
[settings module path, root urls.py, wsgi/asgi path, important middleware]
```

### .claude/memory/stack.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Stack Details — [PROJECT_NAME]

## Dependencies and Their Role
[Each non-trivial package: name — what it does in this project]

## DRF Setup
[If DRF: default_authentication_classes, default_permission_classes from settings; pagination class if set]

## Auth Implementation
[JWT: simplejwt config, token obtain URL; Session: login URL; Token: DRF token config]

## Celery Setup (if detected)
[Broker URL env var, task autodiscovery, beat schedule if present]

## External Services
[Only detected: Redis config key, S3 bucket/region env vars, Stripe key env var, Sentry DSN env var]
```

### .claude/memory/conventions.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Conventions — [PROJECT_NAME]

## App Organization
[How apps are structured — one model per file or all in models.py, etc.]

## ViewSet / View Pattern
[DRF ViewSet vs APIView, how routers are registered in urls.py, actual URL prefix pattern]

## Serializer Pattern
[How serializers are named/organized — include a real example from the codebase]

## Query Pattern
[Manager methods, annotations, select_related/prefetch_related usage found in codebase]

## Test Pattern
[pytest-django / Django TestCase, factory-boy / mixer / model-bakery, fixture style]
```

---

## Phase 5: Rewrite Existing Skills with Project-Specific Code

For each file in `.claude/skills/*/SKILL.md`:
1. Read current content
2. Replace all generic examples with this project's actual:
   - App names and model names from MODEL_NAMES
   - Import paths matching actual project layout
   - Settings module path
   - ViewSet/serializer naming from actual codebase
3. Keep structure, replace placeholders

---

## Phase 6: Add New Skills for Detected Libraries

Create `.claude/skills/<name>/SKILL.md` for each detected lib not already in `.claude/skills/`:

**celery → celery-tasks:**
Cover: task definition, delay vs apply_async, shared_task, beat schedule, retry logic, using actual broker config from settings.

**channels → websocket-patterns:**
Cover: consumer setup, routing, channel layers config, authentication over WebSocket.

**simplejwt / djoser → jwt-auth:**
Cover: token obtain/refresh URLs, custom claims, protecting views, actual token header format used.

**boto3 / django-storages → s3-storage:**
Cover: DEFAULT_FILE_STORAGE setting, media file upload, presigned URL generation.

**sentry-sdk → observability:**
Cover: sentry init in settings, custom context, performance monitoring.

**redis (as cache) → redis-cache:**
Cover: cache backend config, cache.get/set patterns, cache_page decorator, cache invalidation.

**factory-boy / model-bakery → test-factories:**
Cover: factory class pattern, using factories in tests, subfactory for FKs, actual model examples.

---

## Phase 7: Update Commands with Project Paths

Update each `.claude/commands/` file:
- Replace `<appname>` placeholders with first app in LOCAL_APPS
- Replace `python manage.py test` with [TEST_CMD]
- Replace generic model examples with first name from MODEL_NAMES
- Replace `python manage.py makemigrations` / `migrate` with [MAKEMIGRATIONS_CMD] / [MIGRATE_CMD]
- Update any URL prefix examples to match actual URL patterns found

---

## Phase 8: Update .claude/rules/

Rewrite `.claude/rules/coding-standards.md` with:
- Actual linter and version detected
- Line length from config
- Import ordering tool if configured (isort, ruff I)
- Type checking if configured (mypy, pyright)
- Django-specific rules derived from reading the actual codebase
- DRF-specific rules if DRF is present

---

## Phase 9: Report

```
✓ Rewrote .claude/CLAUDE.md — [PROJECT_NAME] ([N] apps, [N] models)
✓ Created .claude/memory/project.md
✓ Created .claude/memory/stack.md
✓ Created .claude/memory/conventions.md
✓ Updated N skills with project-specific code examples
✓ Added new skills: [list or "none"]
✓ Updated N commands with actual paths
✓ Rewrote .claude/rules/coding-standards.md

.claude/ is now tuned for [PROJECT_NAME].
Run /claude-fit again after adding new apps or major dependencies.
```
