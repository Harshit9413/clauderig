---
name: claude-fit
description: Deep-scan this PHP project and rebuild .claude/ to be fully project-specific.
---

# /claude-fit

You are performing a **complete project analysis** to transform this `.claude/` folder from generic templates into a project-specific tool. Work through every phase completely without skipping.

---

## Phase 1: Project Discovery

Read every file below that exists (use the Read tool):

**Dependency files:**
`composer.json`, `composer.lock` (package names only, not full lock)

**Laravel entry points:**
`artisan`, `bootstrap/app.php`, `app/Http/Kernel.php`, `routes/api.php`, `routes/web.php`

**Config:**
`config/app.php`, `config/auth.php`, `config/database.php`, `config/cache.php`, `config/queue.php`, `.env.example`

**App structure — list and read up to 3 files from each:**
`app/Models/`, `app/Http/Controllers/`, `app/Http/Controllers/Api/`, `app/Services/`, `app/Repositories/`, `app/Http/Requests/`, `app/Http/Resources/`, `app/Policies/`

**Database:**
`database/migrations/` (list only), `database/factories/` (list only)

**Tests:**
`phpunit.xml`, `phpunit.xml.dist`, `tests/Feature/` (up to 3 files), `tests/Unit/` (up to 3 files)

**Tooling:**
`Makefile`, `.github/workflows/`

**Existing .claude/ content:**
`.claude/CLAUDE.md`, list all files in `.claude/skills/`, `.claude/commands/`, `.claude/rules/`, `.claude/memory/`

---

## Phase 2: Extract Project Context

- **PROJECT_NAME** — from `composer.json` name field or directory
- **PURPOSE** — 1–2 sentences from README or `config/app.php`
- **LARAVEL_VERSION** — from `composer.json` require.laravel/framework
- **PHP_VERSION** — from `composer.json` require.php
- **DEV_SERVER_CMD** — `php artisan serve` or docker equivalent if found
- **TEST_CMD** — `php artisan test` or `./vendor/bin/phpunit`
- **LINT_CMD** — `./vendor/bin/pint` / `php-cs-fixer fix` / `phpcs`
- **STATIC_ANALYSIS_CMD** — `./vendor/bin/phpstan analyse` / `./vendor/bin/psalm` if present
- **MODEL_NAMES** — all Eloquent model class names found in `app/Models/`
- **DATABASE** — MySQL / PostgreSQL / SQLite (from `config/database.php` default or `.env.example`)
- **AUTH_DRIVER** — Sanctum / Passport / JWT (tymon) / None
- **CACHE_DRIVER** — Redis / Memcached / File / None
- **QUEUE_DRIVER** — Redis / Database / SQS / None
- **API_PREFIX** — from `routes/api.php` prefix (e.g. `/api/v1`)
- **HAS_REPOSITORIES** — yes/no (`app/Repositories/` exists)
- **HAS_SERVICES** — yes/no (`app/Services/` exists)
- **HAS_RESOURCES** — yes/no (`app/Http/Resources/` exists)
- **EXTRA_LIBS** — other notable composer packages

---

## Phase 3: Fully Rewrite .claude/CLAUDE.md

**Replace** the entire contents of `.claude/CLAUDE.md`:

```
# Project Rules — [PROJECT_NAME]

## Stack
PHP [PHP_VERSION], Laravel [LARAVEL_VERSION], [DATABASE], [AUTH_DRIVER] auth

## Dev Commands
- Start:           [DEV_SERVER_CMD]
- Test:            [TEST_CMD]
- Lint:            [LINT_CMD]
- Static analysis: [STATIC_ANALYSIS_CMD or "none configured"]
- Migrate:         php artisan migrate
- Seed:            php artisan db:seed
- Cache clear:     php artisan optimize:clear

## Project Structure
[Actual layout — only paths that exist]
- app/Models/ — Eloquent models
- app/Http/Controllers/ — [API-only / web+API based on routes found]
- [app/Services/ if HAS_SERVICES] — business logic
- [app/Repositories/ if HAS_REPOSITORIES] — data access
- [app/Http/Resources/ if HAS_RESOURCES] — API response transformers
- app/Http/Requests/ — form validation
- routes/api.php — API routes ([API_PREFIX])
- database/migrations/ — schema migrations

## Models
[MODEL_NAMES — one per line with table name and key relationships if detected]

## Auth ([AUTH_DRIVER])
[Token issuance endpoint. Middleware name. Guard name from config/auth.php.]

## API Conventions
[URL prefix: [API_PREFIX]. Response format. Pagination style if detected.]

## Code Style
[Detected tool: Pint/php-cs-fixer. Strict types usage in codebase. PSR-12.]

## Always Do
[Derive from actual codebase patterns found]

## Never Do
[Derive from codebase conventions]

## Testing
[TEST_CMD]. Feature tests in tests/Feature/, Unit in tests/Unit/. Factory usage.

## MCP Servers
[Postgres MCP if DATABASE is postgres; GitHub MCP always; Filesystem MCP always]
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
- Auth:       [AUTH_DRIVER]
- Cache:      [CACHE_DRIVER]
- Queue:      [QUEUE_DRIVER]

## Models
[MODEL_NAMES — name, table, key relationships]

## Route Overview
[Describe route structure: api.php groups, middleware applied, route names]

## Key Files
[Kernel.php, auth config, important service providers, key middleware classes]
```

### .claude/memory/stack.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Stack Details — [PROJECT_NAME]

## Composer Dependencies and Their Role
[Each non-framework package: name — what it does in this project]

## Auth Implementation ([AUTH_DRIVER])
[Token issuance endpoint. Middleware name. Guard config. Token storage approach.]

## Queue Setup
[Driver: [QUEUE_DRIVER]. Jobs in app/Jobs/. Dispatch pattern. Horizon if detected.]

## Cache Setup
[Driver: [CACHE_DRIVER]. Cache facade patterns. Tags if Redis.]

## External Services
[Only detected: Stripe env vars, AWS config, mail driver, SMS provider, Sentry DSN]
```

### .claude/memory/conventions.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Conventions — [PROJECT_NAME]

## Controller Pattern
[Resource / invokable / API-only. Route model binding. Response format.]

## Service / Repository Pattern
[If present: injection via constructor, naming, what each layer owns]

## Validation
[Form Requests / inline validate() — derive from actual controllers]

## API Resources
[Resource structure, collection usage, conditional attributes in codebase]

## Test Pattern
[RefreshDatabase, factory patterns, actingAs(), assertion style from actual tests]
```

---

## Phase 5: Rewrite Existing Skills with Project-Specific Code

For each file in `.claude/skills/*/SKILL.md`:
1. Read current content
2. Replace examples with this project's actual:
   - Model names from MODEL_NAMES
   - Namespace from `composer.json` autoload PSR-4
   - Auth guard from `config/auth.php`
   - Database connection name from `config/database.php`
3. Keep structure, replace all generic placeholders

---

## Phase 6: Add New Skills for Detected Libraries

Create `.claude/skills/<name>/SKILL.md` for each detected lib not already present:

**sanctum → sanctum-auth:** Token issuance, SPA auth, middleware, ability tokens, testing with actingAs. Use actual model names.

**passport → passport-oauth:** Client credentials, personal access tokens, scopes, middleware.

**spatie/laravel-permission → role-permissions:** Assigning roles, checking permissions, middleware, seeding roles.

**spatie/laravel-query-builder → query-builder:** Filters, sorts, includes, pagination with actual model examples.

**laravel/horizon → queue-horizon:** Job monitoring, supervisor config, queue priorities.

**maatwebsite/excel → excel-import-export:** Export class, import class, chunked reading.

**sentry/sentry-laravel → observability:** Init in app.php, custom context, performance tracing.

**league/flysystem-aws-s3-v3 → s3-storage:** Disk config, Storage facade upload, presigned URLs.

**predis/predis → redis-cache:** Cache facade, remember pattern, tags, pub/sub if used.

---

## Phase 7: Update Commands with Project Paths

Update each `.claude/commands/` file:
- Replace generic `Post` / `Product` with first name from MODEL_NAMES
- Replace `App\Models\` if project uses different namespace
- Replace test command with [TEST_CMD]
- Replace dev server with [DEV_SERVER_CMD]
- Update route prefix to [API_PREFIX]
- Add `--api` to `make:controller` if project is API-only

---

## Phase 8: Update .claude/rules/

Rewrite `.claude/rules/coding-standards.md` with:
- Actual PHP version and features available
- Strict types: detected from codebase
- Actual linting tool and config path
- Static analysis level from phpstan.neon or psalm.xml
- Naming conventions from actual class names
- PSR compliance level detected

---

## Phase 9: Report

```
✓ Rewrote .claude/CLAUDE.md — [PROJECT_NAME] ([N] models, [AUTH_DRIVER] auth)
✓ Created .claude/memory/project.md
✓ Created .claude/memory/stack.md
✓ Created .claude/memory/conventions.md
✓ Updated N skills with project-specific code examples
✓ Added new skills: [list or "none"]
✓ Updated N commands with actual paths
✓ Rewrote .claude/rules/coding-standards.md

.claude/ is now tuned for [PROJECT_NAME].
Run /claude-fit again after adding major new packages.
```
