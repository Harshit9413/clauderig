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
