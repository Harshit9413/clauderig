# Project Rules — clauderig

## Stack
Python 3.10+, Typer 0.12+, Rich 13+, asyncio (stdlib), PyInstaller (binary builds), pytest 8+ + pytest-cov 5+.

No database, no ORM, no web framework.

## Dev Commands
- Install:  `pip install -e .`
- Run CLI:  `claude-setup init` (or `python -m clauderig`)
- Test:     `pytest -xvs`
- Coverage: `pytest --cov=clauderig --cov-report=term-missing`
- Lint:     `ruff check .`
- Format:   `ruff format .`
- Build PyPI pkg: `python -m build`
- Build binary: `bash build-macos.sh` / `bash build-linux.sh`

## Project Structure
- `src/clauderig/cli.py` — Typer app, three commands: `init`, `list`, `version`
- `src/clauderig/installer.py` — template copy logic, `InstallResult` dataclass, async MCP probing
- `src/clauderig/analyzer.py` — multi-signal stack/framework/language detection
- `src/clauderig/templates/` — five stack-specific `.claude/` template trees
- `src/clauderig/__init__.py` — version via `importlib.metadata`
- `clauderig.spec` — PyInstaller spec (bundles templates as zip)
- `build-macos.sh`, `build-linux.sh` — binary release scripts

## Supported Stacks (template keys)
- `python-fastapi`
- `python-django`
- `php`
- `react-web`
- `react-native`

## Code Style
- PEP 8. Use `ruff` for linting and formatting.
- All functions must have type hints and return type declarations.
- Use `from __future__ import annotations` in every source file.
- No bare `except:` — always catch specific exception types.
- Use `Path` (pathlib) everywhere — never `os.path`.

## Conventions Detected in This Codebase
- CLI commands are decorated with `@app.command()` on the single `typer.Typer` instance in `cli.py`
- Template resolution goes through `_template_src(stack)` in `installer.py` — frozen (PyInstaller) vs dev paths handled there
- Stack detection uses a scoring dict in `analyzer.py`; the highest-scoring key wins
- Interactive prompts use `rich.prompt.Prompt` and `rich.prompt.Confirm`; non-interactive paths skip them
- `InstallResult` is a `@dataclass` — used to return counts and metadata from `install()`
- Async code (MCP probing) lives in `installer.py`; `asyncio.run()` is called once from `install()`

## Always Do
- Keep `cli.py` as pure UI — no filesystem logic there (that belongs in `installer.py`)
- Keep `analyzer.py` pure and side-effect-free — only reads, never writes
- Validate `stack` against `VALID_STACKS` frozenset before any file operations
- Make `dry_run=True` paths completely read-only (no `shutil`, no `chmod`)
- Use `Path` objects, not string concatenation, for all file paths

## Never Do
- No business logic in CLI command functions — delegate to `installer.py`
- No interactive prompts inside `installer.py` or `analyzer.py` — only in `cli.py`
- No hardcoded stack names outside of `VALID_STACKS` and the mapping dicts in `cli.py`
- No `.env` files committed
- No `import *`

## Testing
- No tests exist yet — use `pytest -xvs` when adding them
- Test files go in `tests/`, mirroring `src/clauderig/` structure
- For `installer.py`: use `tmp_path` fixture for isolated file operations
- For `analyzer.py`: build fixture directories in `tmp_path` with known signals
- For `cli.py`: use `typer.testing.CliRunner`

## MCP Servers
- **GitHub MCP** — browse issues/PRs. Needs: `GITHUB_TOKEN` env var.
- **Filesystem MCP** — read/write project files. Pre-configured.
