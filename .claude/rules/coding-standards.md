# clauderig Coding Standards

## Do
- Use `from __future__ import annotations` in every source file
- Type-hint every parameter and return value
- Use `pathlib.Path` for all filesystem paths — never `os.path`
- Keep CLI command functions ≤ 20 lines; delegate to `installer.py`
- Keep `analyzer.py` pure — no filesystem writes, no prompts, no side effects
- Keep prompts and Rich output in `cli.py` only
- Use `ruff check --fix` and `ruff format .` before every commit
- Validate `stack` against `VALID_STACKS` before any file operation
- Use `@dataclass` for structured return values (see `InstallResult`)
- Catch specific exception types: `(OSError, json.JSONDecodeError)`, `(asyncio.TimeoutError, FileNotFoundError, OSError)`

## Don't
- Don't use `os.path` — use `Path` everywhere
- Don't put prompts or user interaction in `installer.py` or `analyzer.py`
- Don't put filesystem logic in `cli.py`
- Don't catch broad `except Exception` or bare `except:`
- Don't hardcode stack names as strings outside `VALID_STACKS` and the mapping dicts
- Don't commit `.env` or secrets
- Don't use `import *`
- Don't use synchronous subprocess calls where the async version exists

## Linter
- `ruff check .` — linting
- `ruff format .` — formatting
- No explicit line-length override detected; ruff default (88) applies

## Testing
- `pytest -xvs` — run tests (stop on first failure, verbose)
- `pytest --cov=clauderig --cov-report=term-missing` — with coverage
- Use `tmp_path` for filesystem isolation
- Use `typer.testing.CliRunner` for CLI tests
- Test naming: `test_<what>_<expected_outcome>`
