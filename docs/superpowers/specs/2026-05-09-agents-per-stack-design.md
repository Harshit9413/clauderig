# Design: Per-Stack Claude Code Sub-Agents

**Date:** 2026-05-09  
**Status:** Approved

---

## Problem

Each clauderig template installs stack-specific skills, hooks, and commands but no agent definitions. Users working in a FastAPI project and a PHP project get the same generic Claude Code behaviour — there's no specialised sub-agent that knows, say, how to run Alembic migrations or write PHPUnit tests.

---

## Goal

Add a `.claude/agents/` folder to each of the five stack templates. Each folder contains 6 markdown sub-agent files — 5 shared role/task agents customised for the stack, plus 1 stack-specific specialist. Update `installer.py` and `cli.py` to count and surface the agent count in the install summary.

---

## Agent File Format

Each agent is a Markdown file at `.claude/agents/<name>.md` with YAML frontmatter:

```markdown
---
name: agent-name
description: One sentence — when Claude should delegate to this agent.
tools: Read, Edit, Bash(...)
---

# Role / persona

Short description of the agent's purpose.

## Responsibilities
- ...

## Stack conventions to follow
- ...
```

The `description` field is what Claude Code uses to decide which agent to invoke automatically.

---

## Agents Per Stack

### Shared agents (all 5 stacks — content differs per stack)

| File | Type | Purpose |
|---|---|---|
| `test-writer.md` | Task | Write and update tests following stack's test framework and patterns |
| `code-reviewer.md` | Role | Review code for correctness, style, and stack conventions |
| `security-auditor.md` | Role | Audit for security vulnerabilities relevant to the stack |
| `debugger.md` | Task | Systematic debugging using stack-specific tools and log signals |
| `architect.md` | Role | Design new features following stack's folder/layer conventions |

### Stack-specific 6th agent

| Stack | File | Purpose |
|---|---|---|
| `python-fastapi` | `db-migration.md` | Create, apply, and roll back Alembic migrations |
| `python-django` | `orm-optimizer.md` | Fix N+1 queries, add `select_related`/`prefetch_related`, optimise ORM |
| `php` | `artisan-helper.md` | Generate controllers, models, requests, migrations via `php artisan` |
| `react-web` | `performance-optimizer.md` | Memoization, bundle size, Lighthouse audit, lazy loading |
| `react-native` | `navigation-designer.md` | React Navigation stack/tab/drawer setup and deep-link wiring |

---

## Per-Stack Agent Details

### python-fastapi

- **test-writer**: pytest + pytest-asyncio + httpx.AsyncClient, one test per endpoint behaviour, `tmp_path` for file isolation
- **code-reviewer**: Pydantic v2, async route handlers, service-layer separation, no business logic in routes, ruff clean
- **security-auditor**: HTTPBearer token validation, CORS origins, dependency injection for auth, no secrets in code
- **debugger**: SQLAlchemy async session errors, Alembic revision conflicts, uvicorn startup failures, httpx response tracing
- **architect**: Resource-per-file router layout, schemas/services/models separation, `Depends()` patterns, lifespan events
- **db-migration**: `alembic revision --autogenerate`, `alembic upgrade head`, rollback with `alembic downgrade -1`, conflict resolution

### python-django

- **test-writer**: `django.test.TestCase`, `Client` and `APIClient` (DRF), `factory_boy` factories, `pytest-django`
- **code-reviewer**: DRF serializer patterns, `get_queryset` overrides, permission classes, view/serializer separation
- **security-auditor**: CSRF middleware, `@login_required`, SQL injection via raw queries, `DEBUG=False` in prod
- **debugger**: `manage.py shell` queries, migration conflicts (`--merge`), DRF 400/403 response introspection
- **architect**: Apps-per-domain layout, model/view/serializer/URL layering, settings split (base/dev/prod)
- **orm-optimizer**: `select_related`, `prefetch_related`, `only()`/`defer()`, `annotate()` vs Python-level aggregation, Django Debug Toolbar hints

### php

- **test-writer**: PHPUnit Feature tests in `tests/Feature/`, Unit tests in `tests/Unit/`, `factory()->create()`, `assertStatus()`, `assertJson()`
- **code-reviewer**: PSR-12 style, `declare(strict_types=1)`, return type declarations, Form Request validation, service classes
- **security-auditor**: `$request->validated()` usage, CSRF tokens on web routes, no `DB::raw()` with user input, `.env` secrets check
- **debugger**: `php artisan tinker`, Laravel log tailing, queue failures, migration rollback, `dd()` placement
- **architect**: Laravel directory conventions, service/repository pattern, Form Request per action, route grouping
- **artisan-helper**: `make:controller`, `make:model -mfs`, `make:request`, `make:migration`, `migrate:fresh --seed`

### react-web

- **test-writer**: Vitest + React Testing Library, `render()` + `userEvent`, `screen.getBy*` queries, mock API with `msw`
- **code-reviewer**: TypeScript strict (no `any`), props interfaces, custom hooks for data fetching, no direct DOM manipulation
- **security-auditor**: XSS via `dangerouslySetInnerHTML`, CSP headers, dependency audit (`npm audit`), secrets in env vars
- **debugger**: React DevTools hints, `useEffect` dependency issues, stale closure detection, network tab guidance
- **architect**: Component/page/hook/api folder structure, Context boundary design, Tailwind class organisation
- **performance-optimizer**: `useMemo`/`useCallback` placement, `React.lazy()`, bundle analysis, Lighthouse Core Web Vitals

### react-native

- **test-writer**: Jest + React Native Testing Library, `render()`, `fireEvent`, `waitFor`, Expo test setup
- **code-reviewer**: RN-specific TypeScript, StyleSheet over inline styles, platform-specific code (`Platform.OS`), accessibility props
- **security-auditor**: Expo SecureStore for tokens, no hardcoded API keys, deep-link validation, certificate pinning awareness
- **debugger**: Metro bundler errors, native module linking failures, Expo Go vs bare workflow differences, Hermes stack traces
- **architect**: Screen/component/hook/service separation, Expo Router or React Navigation stack design
- **navigation-designer**: Stack, Tab, Drawer navigator setup, typed route params, deep-link config, `useNavigation` patterns

---

## Python Code Changes

### `installer.py`

```python
@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    agents_count: int          # NEW
    mcps_configured: list[str]
    target_path: Path
```

In `install()`:
```python
return InstallResult(
    commands_count=_count_dir(dst / "commands"),
    skills_count=_count_dir(dst / "skills"),
    hooks_count=_count_dir(dst / "hooks"),
    ruleset_count=_count_dir(dst / "rules"),
    agents_count=_count_dir(dst / "agents"),   # NEW
    mcps_configured=_get_mcps(dst / "settings.json"),
    target_path=dst,
)
```

The `dry_run` path also returns `agents_count=0` like the other counts.

### `cli.py`

Add agents to the install summary Rich table/output:
```
  agents   : 6
```

---

## File Count

| Stack | Agent files |
|---|---|
| python-fastapi | 6 |
| python-django | 6 |
| php | 6 |
| react-web | 6 |
| react-native | 6 |
| **Total** | **30** |

Plus changes to `installer.py` and `cli.py`.

---

## Out of Scope

- No changes to `analyzer.py`
- No changes to existing skills, hooks, commands, or rules
- No new CLI commands
- Agents are templates — users edit them after `clauderig init`
