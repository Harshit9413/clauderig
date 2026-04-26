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
