# clauderig — Dev Reference

## Commands

| Task | Command |
|------|---------|
| Run tests | `pytest -xvs` |
| Coverage | `pytest --cov=clauderig --cov-report=term-missing` |
| Lint | `ruff check .` |
| Format | `ruff format .` |
| Type-check | `mypy src/clauderig` |
| Build macOS binary | `bash build-macos.sh` |
| Build Linux binary | `bash build-linux.sh` |
| Build PyPI package | `python -m build` |
| Install dev | `pip install -e .` |

## PyInstaller Watch-outs

- **Template bundling**: Templates are bundled as `templates_bundle.zip`, NOT via `datas`. Reading from `sys._MEIPASS` breaks on frozen builds — use `_template_src()` in `installer.py` which handles both frozen and dev paths.
- **sys.frozen**: Always check `getattr(sys, 'frozen', False)` before resolving paths; dev and frozen paths differ.
- **Hidden imports**: If adding new stdlib/third-party imports, verify they appear in the frozen binary. Add to `hiddenimports` in `clauderig.spec` if missing.
- **No relative imports from __main__**: PyInstaller entry point is `__main__.py` — avoid relative imports there.
- **rthook**: `rthook_clauderig.py` runs at binary startup; keep it minimal and side-effect-free.
- **Binary size**: Avoid importing large optional packages at module level — lazy-import inside functions when possible.

## Python 3.12 Conventions

- Use `type X = Y` syntax for type aliases (PEP 695) instead of `TypeAlias`
- Use `from __future__ import annotations` for forward references until 3.12+ is the baseline
- `tomllib` is stdlib (3.11+) — no need for the `tomli` backport
- `ExceptionGroup` / `except*` available for parallel error handling
- `asyncio.TaskGroup` preferred over `gather()` for structured concurrency
- `match`/`case` (3.10+) for multi-branch dispatch instead of long `if/elif` chains
- `pathlib.Path` everywhere — `os.path` is legacy
