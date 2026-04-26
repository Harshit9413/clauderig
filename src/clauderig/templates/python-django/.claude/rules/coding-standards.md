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
