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
