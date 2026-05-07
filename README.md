# clauderig

**Bootstrap a production-grade `.claude/` setup into any project — one command.**

[![PyPI](https://img.shields.io/pypi/v/clauderig)](https://pypi.org/project/clauderig/)
[![Python](https://img.shields.io/pypi/pyversions/clauderig)](https://pypi.org/project/clauderig/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://claude.ai/chat/LICENSE)

---

## Install

### Linux (Debian / Ubuntu)

```bash
# 1. Add the APT repository (only needs to be done once)
echo "deb [trusted=yes] https://harshit9413.github.io/apt-repo stable main" | \
    sudo tee /etc/apt/sources.list.d/clauderig.list

# 2. Update and install
sudo apt update && sudo apt install clauderig

# 3. Run
cd ~/projects/my-django-app
clauderig init

# To update
sudo apt update && sudo apt upgrade clauderig
```

### macOS

```bash
# 1. Add the Homebrew tap (only needs to be done once)
brew tap harshit9413/clauderig

# 2. Install
brew install clauderig

# 3. Go to any project
cd ~/projects/my-fastapi-app

# 4. Run clauderig
claude-setup init
# → Auto-detects: "Python → FastAPI"
# → Asks: "Use detected stack? [Y/n]"
# → Press Y
# → Creates .claude/ folder in your project
```

### Via PyPI (all platforms)

```bash
pipx install clauderig
cd my-project
claude-setup init
```

> **Note:** Installed via `pip` or `pipx`? Use `claude-setup`.
> Installed via `apt` or `brew`? Use `clauderig`.

Requires  **Python 3.10+** .

---

## Overview

`clauderig` is a CLI tool that scaffolds a complete `.claude/` directory into any project. Instead of manually configuring Claude Code from scratch — writing `settings.json`, creating slash commands, adding skill docs — you run one command and get a fully wired setup tailored to your tech stack.

It ships real, opinionated content: actual code patterns, working MCP server configs, an auto-lint hook, and slash commands that do real things like generate endpoints, run migrations, and review your branch.

---

## What Gets Scaffolded

```
.claude/
├── settings.json            ← permissions, MCP servers, auto-lint hook
├── CLAUDE.md                ← stack rules Claude reads every session
├── commands/
│   ├── claude-fit.md        ← personalises your .claude/ to your exact project
│   └── <stack commands>.md  ← add endpoint / add model / review / etc.
├── skills/
│   └── <skill>/SKILL.md     ← real code examples for your stack's patterns
├── hooks/
│   ├── post-edit-lint.sh    ← runs your linter after every file edit
│   └── setup-mcps.sh        ← installs MCP npm prerequisites
└── rules/
    └── coding-standards.md  ← dos and don'ts for your stack
```

---

## Supported Stacks

| Stack             | Flags                                     | Commands | Skills | MCPs |
| ----------------- | ----------------------------------------- | -------- | ------ | ---- |
| Python → FastAPI | `--lang python --framework fastapi`     | 5        | 3      | 3    |
| Python → Django  | `--lang python --framework django`      | 5        | 3      | 3    |
| PHP (Laravel)     | `--lang php`                            | 4        | 2      | 3    |
| React → Web      | `--lang react --framework reactjs`      | 4        | 3      | 3    |
| React → Native   | `--lang react --framework react-native` | 4        | 3      | 2    |

---

---

## Usage

### `claude-setup init`

Scaffolds `.claude/` into your project.

```bash
# Interactive — asks you to choose stack and options
claude-setup init

# Non-interactive
claude-setup init --lang python --framework fastapi --target .
claude-setup init --lang python --framework django --target .
claude-setup init --lang php --target .
claude-setup init --lang react --framework reactjs --target .
claude-setup init --lang react --framework react-native --target .

# Force overwrite an existing .claude/ directory
claude-setup init --lang react --framework reactjs --force
```

### `claude-setup list`

Lists all supported stacks and their flags.

### `claude-setup version`

Prints the installed version.

---

## MCP Servers

Each stack comes with MCP servers pre-wired in `settings.json`. Claude Code reads these automatically.

| MCP Server | FastAPI | Django | PHP | React Web | React Native |
| ---------- | ------- | ------ | --- | --------- | ------------ |
| GitHub     | ✓      | ✓     | ✓  | ✓        | ✓           |
| Filesystem | ✓      | ✓     | ✓  | ✓        | ✓           |
| PostgreSQL | ✓      | ✓     | ✓  |           |              |
| Playwright |         |        |     | ✓        |              |

**One-time setup:** run `.claude/hooks/setup-mcps.sh` after init to install the required npm packages.

**Environment variables needed:**

* `GITHUB_TOKEN` — for the GitHub MCP server
* `DATABASE_URL` — for the PostgreSQL MCP server

---

## Slash Commands

Run these inside Claude Code after `claude-setup init`.

### Python → FastAPI

| Command           | What it does                                                                          |
| ----------------- | ------------------------------------------------------------------------------------- |
| `/add-endpoint` | Creates router, Pydantic schemas, service layer, and a pytest test for a new endpoint |
| `/add-test`     | Writes an async test using `pytest-asyncio`+`httpx.AsyncClient`                   |
| `/db-migration` | Generates an Alembic migration, shows the diff, confirms, then applies it             |
| `/review`       | Diffs your branch, checks type hints, runs `pytest`and `ruff`, reports issues     |
| `/claude-fit`   | Deep-scans your project and rewrites `.claude/`to match it exactly                  |

### Python → Django

| Command            | What it does                                                                          |
| ------------------ | ------------------------------------------------------------------------------------- |
| `/add-model`     | Adds a model, runs `makemigrations`, shows the file, applies it, registers in admin |
| `/add-view`      | Creates a DRF view, serializer, URL pattern, and test using `APIClient`             |
| `/run-migration` | Makes a schema change, generates migration, confirms, applies it                      |
| `/review`        | Diffs branch, checks for N+1 queries, runs `python manage.py test`and `ruff`      |
| `/claude-fit`    | Deep-scans your project and rewrites `.claude/`to match it exactly                  |

### PHP → Laravel

| Command             | What it does                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------ |
| `/add-controller` | Generates controller, Form Request with validation rules, routes, and PHPUnit feature test |
| `/add-test`       | Writes a feature or unit test using factories and `actingAs()`                           |
| `/review`         | Diffs branch, checks `strict_types`, no raw SQL, runs `php artisan test`               |
| `/claude-fit`     | Deep-scans your project and rewrites `.claude/`to match it exactly                       |

### React → Web

| Command            | What it does                                                                         |
| ------------------ | ------------------------------------------------------------------------------------ |
| `/add-component` | Creates a typed component with props interface, Tailwind styling, and test           |
| `/add-hook`      | Creates a custom hook with TypeScript types, loading/error states, and test          |
| `/review`        | Diffs branch, runs `tsc --noEmit`, checks for `any`, runs `npm test`and ESLint |
| `/claude-fit`    | Deep-scans your project and rewrites `.claude/`to match it exactly                 |

### React → Native

| Command            | What it does                                                                 |
| ------------------ | ---------------------------------------------------------------------------- |
| `/add-component` | Creates a typed RN component with `StyleSheet.create`and test              |
| `/add-screen`    | Creates a screen, registers it in the navigator, writes a render test        |
| `/review`        | Checks safe-area handling, platform guards,`StyleSheet.create`, runs tests |
| `/claude-fit`    | Deep-scans your project and rewrites `.claude/`to match it exactly         |

---

## The `/claude-fit` Command

`/claude-fit` is the most powerful command clauderig ships. Run it once after init to turn your generic `.claude/` into one that knows your exact project.

It works in 9 phases:

1. **Discovery** — reads your dependency files, entry points, source directories, and config
2. **Context extraction** — maps your real folder paths, model names, dev/test/lint commands, auth approach, database, and detected libraries
3. **Rewrites `CLAUDE.md`** — replaces the generic template with your actual commands, folder structure, and conventions
4. **Creates `.claude/memory/`** — generates `project.md`, `stack.md`, and `conventions.md` with project-specific reference info Claude can use across sessions
5. **Rewrites skills** — updates all code examples to use your real import paths, model names, and config locations
6. **Adds new skills** — detects libraries in your project not covered by base skills and creates new `SKILL.md` files for them (e.g. Redis, Celery, React Query, Zustand, Sanctum, EAS, and more)
7. **Updates command paths** — replaces all generic folder paths and example names in commands with your real values
8. **Rewrites coding standards** — updates `rules/coding-standards.md` with your actual linter, formatter, and TypeScript config
9. **Prints a summary** — shows exactly what was created or changed

---

## Skills Included

### Python → FastAPI

* **`fastapi-patterns`** — router organisation, `Depends()`, error handlers, `lifespan`, background tasks
* **`pydantic-models`** — Pydantic v2 schemas, `field_validator`, `model_validator`, `ConfigDict`, settings management
* **`async-db`** — SQLAlchemy 2.x async sessions, typed mapped columns, service pattern, transactions, `selectinload`

### Python → Django

* **`django-orm`** — queryset patterns, `select_related`/`prefetch_related`, custom managers, `@transaction.atomic`, bulk ops
* **`django-views`** — DRF `ModelViewSet`, `APIView`, custom `BasePermission`, pagination
* **`drf-serializers`** — `ModelSerializer`, validation, nested serializers, `SerializerMethodField`, write nested M2M

### PHP → Laravel

* **`psr-standards`** — PSR-12 style, `declare(strict_types=1)`, constructor promotion, return types, nullable/union types
* **`composer-deps`** — version constraints, useful commands, lock file discipline, auditing for vulnerabilities

### React → Web

* **`react-hooks`** — data fetching with cancellation, `useMemo`, `useCallback`, `useRef`, custom form hook
* **`state-management`** — Context for auth/theme, Zustand for client state, React Query for server state
* **`tailwind-patterns`** — responsive layouts, card and button patterns, form inputs, `clsx`, dark mode

### React → Native

* **`expo-patterns`** — dynamic `app.config.js`, env vars via `expo-constants`, `SecureStore`, EAS build
* **`native-modules`** — camera, location, image picker, `Platform.select` styles, permission pattern
* **`navigation-setup`** — React Navigation v6, typed `RootStackParamList`, stack and tab navigators, `useNavigation`

---

## Building from Source

### Linux — `.deb` package

```bash
bash build-linux.sh
# Output: dist/clauderig_1.0.10_amd64.deb

# Override version
APP_VERSION=1.1.0 bash build-linux.sh

# Skip PyInstaller, repackage only
SKIP_BUILD=1 bash build-linux.sh
```

### macOS — `.zip` archive

```bash
bash build-macos.sh
# Output: dist/clauderig_1.0.10_macos_arm64.zip
```

Both scripts run PyInstaller using `clauderig.spec`, bundle `templates_bundle.zip` inside the binary, and produce a single self-contained executable. At runtime, `rthook_clauderig.py` extracts the templates zip so the app can find its templates normally.

### One-line installer

```bash
curl -fsSL https://harshit9413.github.io/apt-repo/install.sh | bash
```

Adds the apt repo and installs via `apt` on Linux. Installs via Homebrew on macOS.

---

## Publishing to PyPI

```bash
python -m build
twine upload --repository testpypi dist/*   # test first
twine upload dist/*                          # production
```

---

## Project Structure

```
clauderig/
├── src/clauderig/
│   ├── cli.py                    # Typer app — claude-setup entry point
│   └── templates/                # One folder per stack
│       ├── python-fastapi/
│       ├── python-django/
│       ├── php/
│       ├── react-web/
│       └── react-native/
├── clauderig.spec                # PyInstaller spec
├── rthook_clauderig.py           # Extracts templates bundle at runtime
├── templates_bundle.zip          # Zipped templates for binary builds
├── MANIFEST.in                   # Includes dotfiles in PyPI sdist
├── build-linux.sh                # Produces .deb
├── build-macos.sh                # Produces .zip
├── install.sh                    # One-line curl installer
├── pyproject.toml
└── requirements.txt
```

---

## Dependencies

| Package   | Version | Purpose                    |
| --------- | ------- | -------------------------- |
| `typer` | ≥ 0.12 | CLI framework              |
| `rich`  | ≥ 13.0 | Terminal output formatting |

Dev extras (`pip install -e ".[dev]"`): `pytest`, `pytest-cov`, `build`, `twine`

---

## Author

**Harshit Jangid** · [GitHub](https://github.com/harshit9413) · [Issues](https://github.com/harshit9413/clauderig/issues)

---

## License

MIT — see [LICENSE](https://claude.ai/chat/LICENSE) for details.
