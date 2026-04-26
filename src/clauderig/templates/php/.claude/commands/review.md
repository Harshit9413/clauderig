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
