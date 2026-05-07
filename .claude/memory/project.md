---
type: project
updated: 2026-05-07
---
# clauderig

A CLI tool that bootstraps a production-grade `.claude/` directory into any project in one command. It auto-detects the tech stack (Python/FastAPI, Python/Django, PHP/Laravel, React Web, React Native) and installs tailored Claude Code configuration: settings.json, CLAUDE.md, slash commands, skill docs, and hooks.

## Quick Reference
- Install for dev: `pip install -e .`
- Run:     `claude-setup init` (PyPI/pipx) or `clauderig init` (apt/brew)
- Tests:   `pytest -xvs`
- Lint:    `ruff check .`
- Build:   `python -m build` (PyPI) / `bash build-macos.sh` (binary)
- Database: None
- Auth:     None
- Cache:    None

## Key Dataclass
- `InstallResult` (`src/clauderig/installer.py`) — returned from `install()`; carries `commands_count`, `skills_count`, `hooks_count`, `ruleset_count`, `mcps_configured`, `target_path`

## Entry Points
- `src/clauderig/cli.py` — `app = typer.Typer(...)` with `init`, `list`, `version` commands
- `src/clauderig/__main__.py` — `app()` for `python -m clauderig`
- `pyproject.toml` `[project.scripts]` — `claude-setup = "clauderig.cli:app"`

## Key Files to Know
1. `src/clauderig/cli.py` — all user-facing CLI logic and interactive prompts
2. `src/clauderig/installer.py` — `install()`, `_template_src()`, async MCP probing
3. `src/clauderig/analyzer.py` — `detect_stack()`, `detect_framework()`, `detect_language()`
4. `src/clauderig/templates/` — five template trees installed into target projects
5. `clauderig.spec` — PyInstaller spec; `templates_bundle.zip` is embedded in the binary
6. `build-macos.sh` / `build-linux.sh` — binary release pipeline
7. `pyproject.toml` — package metadata, dependencies, entry point
