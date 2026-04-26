# clauderig — Design Spec

**Date:** 2026-04-25
**Status:** Approved
**CLI command:** `claude-setup` | **Package name:** `clauderig`

---

## 1. What We're Building

A Python CLI package (`clauderig` on PyPI) that bootstraps a production-grade `.claude/` folder into any project with one command. Target user: a developer who has heard of Claude Code but doesn't know how to set up skills, hooks, slash commands, MCP servers, rules, or permissions.

Install `clauderig`, run `claude-setup init`, pick your stack, and get a polished `.claude/` setup instantly — including pre-configured MCP servers and an auto-lint hook.

---

## 2. Project Structure

```
claude_setup_cli/
├── pyproject.toml
├── README.md
├── LICENSE                        (MIT)
├── .gitignore                     (standard Python)
├── MANIFEST.in                    (ensures hidden .claude dirs are in wheel)
├── .github/
│   └── workflows/
│       └── test.yml               (pytest on push/PR, Python 3.10–3.12)
├── src/
│   └── clauderig/
│       ├── __init__.py            (__version__ = "0.1.0")
│       ├── __main__.py            (python -m clauderig)
│       ├── cli.py                 (~120 lines, typer app)
│       ├── installer.py           (~100 lines, install() + async check_prerequisites())
│       ├── analyzer.py            (~60 lines, detect_stack())
│       └── templates/
│           ├── python-fastapi/.claude/
│           ├── python-django/.claude/
│           ├── php/.claude/
│           ├── react-web/.claude/
│           └── react-native/.claude/
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_installer.py
    └── test_analyzer.py
```

---

## 3. CLI Commands (exactly three)

### `claude-setup init`

Interactive (no flags):

```
$ claude-setup init
? Primary language?  [Python / PHP / React]
? Framework?         (only for Python or React)
? Target directory?  [.]
✓ Copied .claude/ to /abs/path
✓ Installed: 4 commands · 3 skills · 2 hooks · 1 ruleset
✓ MCPs pre-configured: github, filesystem, postgres
→ Run `.claude/hooks/setup-mcps.sh` once to install MCP prerequisites
→ Run `claude` and try the /claude-fit slash command
```

Non-interactive flags:

- `--lang {python,php,react}` — required for non-interactive
- `--framework {fastapi,django,reactjs,react-native}` — validated against `--lang`
- `--target PATH` — default `.`
- `--force` — overwrite existing `.claude/` without prompting
- `--dry-run` — print file tree that would be copied, write nothing

**Validation rules:**

- `--lang php` accepts no `--framework` (single stack)
- `--lang python` requires `--framework fastapi` or `django`
- `--lang react` requires `--framework reactjs` or `react-native`
- Mismatched combo (e.g., `--lang php --framework fastapi`) → clean error, exit 1
- Existing `.claude/` without `--force` in interactive mode → `typer.confirm("`.claude/` already exists. Overwrite?")` — user types `y` to proceed, anything else aborts cleanly; in non-interactive (flags provided) → raise `FileExistsError` with message "`.claude/` already exists. Use --force to overwrite."

### `claude-setup list`

Rich table: stack name, commands count, skills count, hooks count, MCP count.

### `claude-setup version`

Prints `clauderig 0.1.0`.

---

## 4. Template Structure (per stack)

Each `.claude/` folder contains:

.claude/
├── settings.json          # permissions + hooks + mcpServers block
├── CLAUDE.md              # stack rules, conventions, MCP docs
├── commands/
 │   ├── claude-fit.md      # the "brain" — instructs Claude to scan & enhance
 │   └── *.md               # 3–4 stack-specific slash commands
├── skills/
 │   └── `<name>`
 │       └── SKILL.md       # YAML frontmatter + 50–150 lines of guidance
├── hooks/
 │   ├── post-edit-lint.sh  # auto-lint on Edit/Write (chmod 755 after copy)
 │   └── setup-mcps.sh      # one-shot prerequisite installer (chmod 755)

└── rules/
    └── coding-standards.md

---

## 5. Per-Stack Commands, Skills, and MCPs

### Python → FastAPI

**Commands:** `claude-fit.md`, `add-endpoint.md`, `add-test.md`, `review.md`, `db-migration.md`
**Skills:** `fastapi-patterns/`, `pydantic-models/`, `async-db/`
**MCPs:** GitHub, Filesystem, PostgreSQL
**Lint hook:** `ruff check --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true`
**Test command in settings.json:** `Bash(pytest:*)`

### Python → Django

**Commands:** `claude-fit.md`, `add-view.md`, `add-model.md`, `run-migration.md`, `review.md`
**Skills:** `django-orm/`, `django-views/`, `drf-serializers/`
**MCPs:** GitHub, Filesystem, PostgreSQL
**Lint hook:** `ruff check --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true`
**Test command in settings.json:** `Bash(python manage.py test:*)`

### PHP

**Commands:** `claude-fit.md`, `add-controller.md`, `add-test.md`, `review.md`
**Skills:** `psr-standards/`, `composer-deps/`
**MCPs:** GitHub, Filesystem, PostgreSQL
**Lint hook:** `php-cs-fixer fix "$CLAUDE_FILE_PATH" 2>/dev/null || true`
**Test command in settings.json:** `Bash(phpunit:*)`

### React → ReactJS (Web)

**Commands:** `claude-fit.md`, `add-component.md`, `add-hook.md`, `review.md`
**Skills:** `react-hooks/`, `tailwind-patterns/`, `state-management/`
**MCPs:** GitHub, Filesystem, Playwright
**Lint hook:** `npx eslint --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true`
**Test command in settings.json:** `Bash(npm test:*)`

### React → React Native

**Commands:** `claude-fit.md`, `add-screen.md`, `add-component.md`, `review.md`
**Skills:** `expo-patterns/`, `navigation-setup/`, `native-modules/`
**MCPs:** GitHub, Filesystem
**Lint hook:** `npx eslint --fix "$CLAUDE_FILE_PATH" 2>/dev/null || true`
**Test command in settings.json:** `Bash(npm test:*)`

---

## 6. settings.json Structure

```json
{
  "permissions": {
    "allow": ["Read", "Edit", "Bash(git:*)", "Bash(<stack-test-cmd>)"],
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

*(Postgres entry present only in FastAPI, Django, PHP templates. Playwright entry replaces Postgres in React Web template. React Native has only github + filesystem.)*
}

```

---

## 7. MCP Strategy (Approach A + C)

**A — Pre-configure in settings.json:** The `mcpServers` block is written into the template's `.claude/settings.json`. Claude Code reads this automatically when the user opens the project. No runtime installs during `claude-setup init`.

**C — Drop `setup-mcps.sh`:** A `hooks/setup-mcps.sh` script ships with each template. It contains `npm install -g` commands for the stack's MCPs (e.g., `npm install -g @modelcontextprotocol/server-postgres`). User runs it once with `bash .claude/hooks/setup-mcps.sh`. The script is idempotent and prints what it's installing.

This means: zero surprise installs, zero conflicts, fully transparent.

**MCP per stack:**
| Stack | MCPs |
|---|---|
| All stacks | `@modelcontextprotocol/server-github`, `@modelcontextprotocol/server-filesystem` |
| Python FastAPI / Django | + `@modelcontextprotocol/server-postgres` |
| PHP | + `@modelcontextprotocol/server-postgres` |
| React Web | + `@playwright/mcp` |
| React Native | GitHub + Filesystem only |

---

## 8. Async Usage

Async is allowed and used where it adds value:

- `installer.py` includes `async def check_prerequisites(mcps: list[str]) -> dict[str, bool]` — concurrently checks if MCP packages are resolvable via `npx --yes --dry-run`.
- Called via `asyncio.run()` from synchronous `install()` after the copy, purely informational.
- Core file-copy (`shutil.copytree`) stays synchronous — no benefit to async there.
- No async in CLI entry points — avoids event loop conflicts for end users.

---

## 9. Key Implementation Files

### `installer.py`
```python
@dataclass
class InstallResult:
    commands_count: int
    skills_count: int
    hooks_count: int
    ruleset_count: int
    mcps_configured: list[str]
    target_path: Path

def install(stack: str, target: Path, force: bool, dry_run: bool) -> InstallResult:
    ...
```

- Locates templates via `importlib.resources.files("clauderig.templates") / stack / ".claude"`
- Uses `shutil.copytree(src, dst, dirs_exist_ok=force)`
- `chmod 0o755` all `.sh` files in `dst/hooks/`
- Returns counts by scanning copied directories

### `analyzer.py`

```python
def detect_stack(path: Path) -> str | None:
    ...
```

Reads marker files (`pyproject.toml`, `requirements.txt`, `manage.py`, `composer.json`, `package.json`, `app.json`) and returns one of the five stack keys or `None`. Pure reads, no side effects. Reserved for future `--auto-detect` flag.

---

## 10. The `/claude-fit` Command

Ships in every stack's `commands/claude-fit.md`. When the user runs `/claude-fit` in Claude Code, Claude itself executes its instructions to:

1. Inventory project root for dependency files
2. Detect actually-used libraries and suggest new skills/commands
3. Read existing `.claude/skills/` and `.claude/commands/` to avoid duplicates
4. Present a numbered checklist of proposed additions
5. Create approved files using the same YAML frontmatter conventions
6. Update `CLAUDE.md` with project-specific context

---

## 11. Tests

- `test_cli.py` — CliRunner: `init --dry-run`, `list`, `version`, bad framework combo → exit 1
- `test_installer.py` — install all 5 stacks into `tmp_path`; assert `settings.json`, `CLAUDE.md`, ≥1 command, ≥1 skill exist; assert `.sh` files are executable (os.access)
- `test_analyzer.py` — fake marker files in `tmp_path`; assert `detect_stack()` returns right key

Target: ~70% coverage. No coverage theater.

---

## 12. Dependencies

```toml
dependencies = ["typer>=0.12", "rich>=13.0"]
```

Everything else: stdlib (`pathlib`, `shutil`, `importlib.resources`, `json`, `re`, `asyncio`, `stat`).

---

## 13. Decisions Noted for README

- CLI command is `claude-setup`, package name is `clauderig`
- PHP has no sub-framework selection (single stack)
- `--auto-detect` is stubbed but not exposed in v1
- MCP prerequisites require `node`/`npx` on PATH
- `setup-mcps.sh` must be run once after `claude-setup init`
- `GITHUB_TOKEN` env var must be set for the GitHub MCP to authenticate
