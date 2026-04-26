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
